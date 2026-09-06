import os
import json
import asyncio
from typing import Dict, List, Set, Optional
from contextlib import asynccontextmanager

from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException, Depends, Query, Body
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel, EmailStr

from backend.database import init_db, get_db_cursor
from backend.auth import hash_password, verify_password, create_session, get_current_user, get_optional_user
from backend.countries import COUNTRIES, OTHER_LANGUAGE_ROOMS, ALL_ROOMS, COUNTRY_MAP
from backend.seed import seed_database
from backend.blogs import BLOG_ARTICLES, BLOG_MAP

# --- Connection Manager for WebSockets ---
class ConnectionManager:
    def __init__(self):
        # room_id -> set of WebSockets
        self.room_connections: Dict[str, Set[WebSocket]] = {c["id"]: set() for c in ALL_ROOMS}
        # user_id -> set of WebSockets (for DMs, presence, squad notifications)
        self.user_connections: Dict[int, Set[WebSocket]] = {}
        # squad_id -> set of WebSockets
        self.squad_connections: Dict[int, Set[WebSocket]] = {}
        # presence WebSockets
        self.presence_connections: Set[WebSocket] = set()

    async def connect_room(self, room_id: str, websocket: WebSocket):
        await websocket.accept()
        if room_id not in self.room_connections:
            self.room_connections[room_id] = set()
        self.room_connections[room_id].add(websocket)

    def disconnect_room(self, room_id: str, websocket: WebSocket):
        if room_id in self.room_connections:
            self.room_connections[room_id].discard(websocket)

    async def broadcast_room(self, room_id: str, message: dict):
        if room_id in self.room_connections:
            dead = set()
            for ws in list(self.room_connections[room_id]):
                try:
                    await ws.send_json(message)
                except Exception:
                    dead.add(ws)
            for ws in dead:
                self.room_connections[room_id].discard(ws)

    async def connect_user(self, user_id: int, websocket: WebSocket):
        await websocket.accept()
        if user_id not in self.user_connections:
            self.user_connections[user_id] = set()
        self.user_connections[user_id].add(websocket)
        self.presence_connections.add(websocket)

    def disconnect_user(self, user_id: int, websocket: WebSocket):
        if user_id in self.user_connections:
            self.user_connections[user_id].discard(websocket)
            if not self.user_connections[user_id]:
                del self.user_connections[user_id]
        self.presence_connections.discard(websocket)

    async def send_user(self, user_id: int, message: dict):
        if user_id in self.user_connections:
            dead = set()
            for ws in list(self.user_connections[user_id]):
                try:
                    await ws.send_json(message)
                except Exception:
                    dead.add(ws)
            for ws in dead:
                self.user_connections[user_id].discard(ws)

    async def connect_squad(self, squad_id: int, websocket: WebSocket):
        await websocket.accept()
        if squad_id not in self.squad_connections:
            self.squad_connections[squad_id] = set()
        self.squad_connections[squad_id].add(websocket)

    def disconnect_squad(self, squad_id: int, websocket: WebSocket):
        if squad_id in self.squad_connections:
            self.squad_connections[squad_id].discard(websocket)

    async def broadcast_squad(self, squad_id: int, message: dict):
        if squad_id in self.squad_connections:
            dead = set()
            for ws in list(self.squad_connections[squad_id]):
                try:
                    await ws.send_json(message)
                except Exception:
                    dead.add(ws)
            for ws in dead:
                self.squad_connections[squad_id].discard(ws)

    async def broadcast_presence(self, message: dict):
        dead = set()
        for ws in list(self.presence_connections):
            try:
                await ws.send_json(message)
            except Exception:
                dead.add(ws)
        for ws in dead:
            self.presence_connections.discard(ws)

manager = ConnectionManager()

# --- Application Lifecycle ---
@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    seed_database()
    yield

app = FastAPI(title="RESPAWN // SQUADFINDER API", version="2.0.0", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Pydantic Request Models ---
class RegisterRequest(BaseModel):
    username: str
    email: str
    password: str
    gamer_tag: str
    country: str = "US"
    primary_game: str = "Valorant"
    platform: str = "PC"
    rank: str = "Diamond"
    avatar: str = "cyber_ninja"

class LoginRequest(BaseModel):
    username_or_email: str
    password: str

class ProfileUpdateRequest(BaseModel):
    gamer_tag: Optional[str] = None
    country: Optional[str] = None
    bio: Optional[str] = None
    avatar: Optional[str] = None
    primary_game: Optional[str] = None
    rank: Optional[str] = None
    platform: Optional[str] = None
    mic_status: Optional[str] = None
    discord_tag: Optional[str] = None

class CreateSquadRequest(BaseModel):
    title: str
    game: str
    mode: str = "Competitive / Ranked"
    rank_req: str = "Any Rank"
    mic_req: str = "Mic Required"
    region: str = "NA (East / West)"
    max_players: int = 5
    discord_voice: Optional[str] = ""
    role: str = "IGL / Shotcaller"

class ChatMessageRequest(BaseModel):
    message: str

class DirectMessageRequest(BaseModel):
    message: str

class FriendActionRequest(BaseModel):
    target: str  # username or gamer_tag

class EndorseRequest(BaseModel):
    category: str  # "Shotcaller", "Tilt-Proof", "Clutch God", "Good Vibes"

# --- Authentication Endpoints ---
@app.post("/api/auth/register")
def register(req: RegisterRequest):
    req_username = req.username.strip().lower()
    req_tag = req.gamer_tag.strip()
    if len(req_username) < 3 or len(req_tag) < 2:
        raise HTTPException(status_code=400, detail="Username and GamerTag must be valid")
    if len(req.password) < 6:
        raise HTTPException(status_code=400, detail="Password must be at least 6 characters")

    with get_db_cursor(commit=True) as cur:
        cur.execute("SELECT id FROM users WHERE username = ? OR email = ?", (req_username, req.email.lower()))
        if cur.fetchone():
            raise HTTPException(status_code=400, detail="Username or email already registered")

        pw_hash = hash_password(req.password)
        cur.execute("""
            INSERT INTO users (username, email, password_hash, gamer_tag, country, primary_game, platform, rank, avatar, is_online)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, 1)
        """, (req_username, req.email.lower(), pw_hash, req_tag, req.country.upper(), req.primary_game, req.platform, req.rank, req.avatar))
        user_id = cur.lastrowid
        token = create_session(user_id, cur=cur)

        cur.execute("SELECT * FROM users WHERE id = ?", (user_id,))
        user_data = dict(cur.fetchone())
        del user_data["password_hash"]

    return {"token": token, "user": user_data}

@app.post("/api/auth/login")
def login(req: LoginRequest):
    identifier = req.username_or_email.strip().lower()
    with get_db_cursor(commit=True) as cur:
        cur.execute("SELECT * FROM users WHERE username = ? OR email = ?", (identifier, identifier))
        row = cur.fetchone()
        if not row:
            raise HTTPException(status_code=400, detail="Invalid username/email or password")
        
        user = dict(row)
        if not verify_password(req.password, user["password_hash"]):
            raise HTTPException(status_code=400, detail="Invalid username/email or password")

        cur.execute("UPDATE users SET is_online = 1 WHERE id = ?", (user["id"],))
        token = create_session(user["id"], cur=cur)
        del user["password_hash"]
        user["is_online"] = 1

    return {"token": token, "user": user}

@app.get("/api/auth/me")
def get_me(user: dict = Depends(get_current_user)):
    user_copy = dict(user)
    if "password_hash" in user_copy:
        del user_copy["password_hash"]
    return user_copy

@app.post("/api/auth/logout")
def logout(user: dict = Depends(get_current_user)):
    with get_db_cursor(commit=True) as cur:
        cur.execute("UPDATE users SET is_online = 0 WHERE id = ?", (user["id"],))
        cur.execute("DELETE FROM sessions WHERE user_id = ?", (user["id"],))
    return {"message": "Logged out successfully"}

# --- National & World Language Chat Rooms ---
@app.get("/api/countries")
def get_countries(category: Optional[str] = None, language: Optional[str] = None):
    # Return national & world language rooms with active player & message counts
    with get_db_cursor(commit=False) as cur:
        cur.execute("""
            SELECT room_id, count(id) as msg_count 
            FROM chat_messages 
            GROUP BY room_id
        """)
        msg_counts = {r["room_id"]: r["msg_count"] for r in cur.fetchall()}

        cur.execute("""
            SELECT country, count(id) as online_count 
            FROM users 
            WHERE is_online = 1 
            GROUP BY country
        """)
        online_counts = {r["country"]: r["online_count"] for r in cur.fetchall()}

    rooms = ALL_ROOMS
    if category and category != "All":
        rooms = [r for r in rooms if r.get("category") == category]
    if language and language != "All":
        lang_low = language.lower()
        rooms = [r for r in rooms if lang_low in r.get("language", "").lower() or lang_low in r.get("language_native", "").lower()]

    result = []
    for c in rooms:
        cid = c["id"]
        ccode = c["code"]
        c_copy = dict(c)
        c_copy["message_count"] = msg_counts.get(cid, 0)
        c_copy["online_count"] = max(online_counts.get(ccode, 0), len(manager.room_connections.get(cid, set())) + (5 if c.get("category") == "other_language" else 3))
        result.append(c_copy)
    return result

@app.get("/api/chat/{room_id}")
def get_room_messages(room_id: str, limit: int = 50):
    room_id = room_id.lower()
    if room_id not in COUNTRY_MAP:
        raise HTTPException(status_code=404, detail="Chat room not found")

    with get_db_cursor(commit=False) as cur:
        cur.execute("""
            SELECT m.*, u.karma_score, u.platform, u.primary_game
            FROM chat_messages m
            LEFT JOIN users u ON m.user_id = u.id
            WHERE m.room_id = ?
            ORDER BY m.timestamp ASC
            LIMIT ?
        """, (room_id, limit))
        messages = [dict(r) for r in cur.fetchall()]

    return {
        "room": COUNTRY_MAP[room_id],
        "messages": messages
    }

@app.post("/api/chat/{room_id}")
async def post_room_message(room_id: str, req: ChatMessageRequest, user: dict = Depends(get_current_user)):
    room_id = room_id.lower()
    if room_id not in COUNTRY_MAP:
        raise HTTPException(status_code=404, detail="Chat room not found")
    
    clean_msg = req.message.strip()
    if not clean_msg:
        raise HTTPException(status_code=400, detail="Message cannot be empty")

    with get_db_cursor(commit=True) as cur:
        cur.execute("""
            INSERT INTO chat_messages (room_id, user_id, gamer_tag, avatar, rank, country, message)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            room_id, user["id"], user["gamer_tag"], user["avatar"], user["rank"], user["country"], clean_msg
        ))
        msg_id = cur.lastrowid
        cur.execute("SELECT * FROM chat_messages WHERE id = ?", (msg_id,))
        new_msg = dict(cur.fetchone())
        new_msg["karma_score"] = user.get("karma_score", 15)
        new_msg["platform"] = user.get("platform", "PC")
        new_msg["primary_game"] = user.get("primary_game", "Valorant")

    # Broadcast via WebSocket to all clients in this nationality room
    await manager.broadcast_room(room_id, {
        "type": "new_chat_message",
        "room_id": room_id,
        "message": new_msg
    })

    return new_msg

# --- LFG Squads / Matchmaking Lobbies ---
@app.get("/api/squads")
def list_squads(game: Optional[str] = None, mode: Optional[str] = None, region: Optional[str] = None):
    query = "SELECT s.*, u.gamer_tag as leader_tag, u.avatar as leader_avatar, u.karma_score as leader_karma FROM squads s JOIN users u ON s.leader_id = u.id WHERE s.status = 'open'"
    params = []

    if game and game != "All Games":
        query += " AND s.game = ?"
        params.append(game)
    if mode and mode != "All Modes":
        query += " AND s.mode = ?"
        params.append(mode)
    if region and region != "All Regions":
        query += " AND s.region = ?"
        params.append(region)

    query += " ORDER BY s.created_at DESC"

    with get_db_cursor(commit=False) as cur:
        cur.execute(query, params)
        squads = [dict(r) for r in cur.fetchall()]

        # Attach members
        for s in squads:
            cur.execute("""
                SELECT sm.*, u.gamer_tag, u.avatar, u.rank, u.platform, u.mic_status, u.karma_score
                FROM squad_members sm
                JOIN users u ON sm.user_id = u.id
                WHERE sm.squad_id = ?
                ORDER BY sm.joined_at ASC
            """, (s["id"],))
            s["members"] = [dict(m) for m in cur.fetchall()]
            s["current_players"] = len(s["members"])

    return squads

@app.post("/api/squads")
async def create_squad(req: CreateSquadRequest, user: dict = Depends(get_current_user)):
    with get_db_cursor(commit=True) as cur:
        # Check if user is already leading an open squad
        cur.execute("SELECT id FROM squads WHERE leader_id = ? AND status = 'open'", (user["id"],))
        existing = cur.fetchone()
        if existing:
            # Auto-close or delete prior squad
            cur.execute("DELETE FROM squads WHERE id = ?", (existing["id"],))

        cur.execute("""
            INSERT INTO squads (leader_id, title, game, mode, rank_req, mic_req, region, max_players, discord_voice, status)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, 'open')
        """, (user["id"], req.title.strip(), req.game, req.mode, req.rank_req, req.mic_req, req.region, req.max_players, req.discord_voice or ""))
        squad_id = cur.lastrowid

        # Insert leader as first squad member
        cur.execute("""
            INSERT INTO squad_members (squad_id, user_id, role, is_ready)
            VALUES (?, ?, ?, ?)
        """, (squad_id, user["id"], req.role, 1))

    return await get_squad_details(squad_id)

@app.get("/api/squads/{squad_id}")
async def get_squad_details(squad_id: int):
    with get_db_cursor(commit=False) as cur:
        cur.execute("""
            SELECT s.*, u.gamer_tag as leader_tag, u.avatar as leader_avatar, u.karma_score as leader_karma
            FROM squads s
            JOIN users u ON s.leader_id = u.id
            WHERE s.id = ?
        """, (squad_id,))
        squad_row = cur.fetchone()
        if not squad_row:
            raise HTTPException(status_code=404, detail="Squad not found")
        
        squad = dict(squad_row)
        cur.execute("""
            SELECT sm.*, u.gamer_tag, u.avatar, u.rank, u.platform, u.mic_status, u.karma_score
            FROM squad_members sm
            JOIN users u ON sm.user_id = u.id
            WHERE sm.squad_id = ?
            ORDER BY sm.joined_at ASC
        """, (squad_id,))
        squad["members"] = [dict(m) for m in cur.fetchall()]
        squad["current_players"] = len(squad["members"])

    return squad

@app.post("/api/squads/{squad_id}/join")
async def join_squad(squad_id: int, role: str = Body(default="Flex", embed=True), user: dict = Depends(get_current_user)):
    with get_db_cursor(commit=True) as cur:
        cur.execute("SELECT * FROM squads WHERE id = ?", (squad_id,))
        squad = cur.fetchone()
        if not squad:
            raise HTTPException(status_code=404, detail="Squad not found")
        
        cur.execute("SELECT count(*) as count FROM squad_members WHERE squad_id = ?", (squad_id,))
        count = cur.fetchone()["count"]
        if count >= squad["max_players"]:
            raise HTTPException(status_code=400, detail="Squad is already full!")

        cur.execute("SELECT * FROM squad_members WHERE squad_id = ? AND user_id = ?", (squad_id, user["id"]))
        if cur.fetchone():
            raise HTTPException(status_code=400, detail="You are already in this squad")

        cur.execute("""
            INSERT INTO squad_members (squad_id, user_id, role, is_ready)
            VALUES (?, ?, ?, ?)
        """, (squad_id, user["id"], role, 0))

    updated_squad = await get_squad_details(squad_id)
    await manager.broadcast_squad(squad_id, {
        "type": "member_joined",
        "squad": updated_squad,
        "gamer_tag": user["gamer_tag"]
    })
    return updated_squad

@app.post("/api/squads/{squad_id}/leave")
async def leave_squad(squad_id: int, user: dict = Depends(get_current_user)):
    with get_db_cursor(commit=True) as cur:
        cur.execute("SELECT * FROM squads WHERE id = ?", (squad_id,))
        squad = cur.fetchone()
        if not squad:
            raise HTTPException(status_code=404, detail="Squad not found")

        if squad["leader_id"] == user["id"]:
            # Leader leaving disbands the squad
            cur.execute("DELETE FROM squads WHERE id = ?", (squad_id,))
            disbanded = True
        else:
            cur.execute("DELETE FROM squad_members WHERE squad_id = ? AND user_id = ?", (squad_id, user["id"]))
            disbanded = False

    if disbanded:
        await manager.broadcast_squad(squad_id, {
            "type": "squad_disbanded",
            "squad_id": squad_id
        })
        return {"status": "disbanded"}
    else:
        updated = await get_squad_details(squad_id)
        await manager.broadcast_squad(squad_id, {
            "type": "member_left",
            "squad": updated,
            "gamer_tag": user["gamer_tag"]
        })
        return updated

@app.post("/api/squads/{squad_id}/ready")
async def toggle_ready(squad_id: int, user: dict = Depends(get_current_user)):
    with get_db_cursor(commit=True) as cur:
        cur.execute("SELECT is_ready FROM squad_members WHERE squad_id = ? AND user_id = ?", (squad_id, user["id"]))
        row = cur.fetchone()
        if not row:
            raise HTTPException(status_code=400, detail="You are not a member of this squad")
        
        new_ready = 0 if row["is_ready"] == 1 else 1
        cur.execute("UPDATE squad_members SET is_ready = ? WHERE squad_id = ? AND user_id = ?", (new_ready, squad_id, user["id"]))

    updated = await get_squad_details(squad_id)
    await manager.broadcast_squad(squad_id, {
        "type": "ready_toggled",
        "user_id": user["id"],
        "gamer_tag": user["gamer_tag"],
        "is_ready": new_ready,
        "squad": updated
    })
    return {"is_ready": new_ready}

@app.post("/api/squads/{squad_id}/ready-check")
async def trigger_ready_check(squad_id: int, user: dict = Depends(get_current_user)):
    with get_db_cursor(commit=False) as cur:
        cur.execute("SELECT leader_id FROM squads WHERE id = ?", (squad_id,))
        squad = cur.fetchone()
        if not squad or squad["leader_id"] != user["id"]:
            raise HTTPException(status_code=403, detail="Only the squad leader can trigger a ready check")

    await manager.broadcast_squad(squad_id, {
        "type": "ready_check_started",
        "squad_id": squad_id,
        "initiated_by": user["gamer_tag"]
    })
    return {"message": "Ready check initiated"}

# --- Direct Messages (1-on-1 Private DMs) ---
@app.get("/api/dms/conversations")
def get_dm_conversations(user: dict = Depends(get_current_user)):
    with get_db_cursor(commit=False) as cur:
        # Get all users who have exchanged DMs with the current user
        cur.execute("""
            SELECT DISTINCT 
                CASE WHEN sender_id = ? THEN receiver_id ELSE sender_id END as other_id
            FROM direct_messages
            WHERE sender_id = ? OR receiver_id = ?
        """, (user["id"], user["id"], user["id"]))
        other_ids = [r["other_id"] for r in cur.fetchall()]

        convos = []
        for oid in other_ids:
            cur.execute("SELECT id, username, gamer_tag, avatar, rank, is_online, karma_score FROM users WHERE id = ?", (oid,))
            partner = cur.fetchone()
            if not partner:
                continue
            
            # Last message
            cur.execute("""
                SELECT message, timestamp, sender_id, is_read
                FROM direct_messages
                WHERE (sender_id = ? AND receiver_id = ?) OR (sender_id = ? AND receiver_id = ?)
                ORDER BY timestamp DESC LIMIT 1
            """, (user["id"], oid, oid, user["id"]))
            last_msg = cur.fetchone()

            # Unread count
            cur.execute("""
                SELECT count(id) as unread
                FROM direct_messages
                WHERE sender_id = ? AND receiver_id = ? AND is_read = 0
            """, (oid, user["id"]))
            unread = cur.fetchone()["unread"]

            convos.append({
                "partner": dict(partner),
                "last_message": dict(last_msg) if last_msg else None,
                "unread_count": unread
            })

    return convos

@app.get("/api/dms/{other_user_id}")
def get_direct_messages(other_user_id: int, user: dict = Depends(get_current_user)):
    with get_db_cursor(commit=True) as cur:
        # Mark messages sent to us as read
        cur.execute("""
            UPDATE direct_messages 
            SET is_read = 1 
            WHERE sender_id = ? AND receiver_id = ?
        """, (other_user_id, user["id"]))

        cur.execute("""
            SELECT dm.*, 
                   s.gamer_tag as sender_tag, s.avatar as sender_avatar,
                   r.gamer_tag as receiver_tag, r.avatar as receiver_avatar
            FROM direct_messages dm
            JOIN users s ON dm.sender_id = s.id
            JOIN users r ON dm.receiver_id = r.id
            WHERE (dm.sender_id = ? AND dm.receiver_id = ?)
               OR (dm.sender_id = ? AND dm.receiver_id = ?)
            ORDER BY dm.timestamp ASC
        """, (user["id"], other_user_id, other_user_id, user["id"]))
        messages = [dict(m) for m in cur.fetchall()]

        cur.execute("SELECT id, username, gamer_tag, avatar, rank, is_online, karma_score, primary_game, platform FROM users WHERE id = ?", (other_user_id,))
        partner = cur.fetchone()

    return {
        "partner": dict(partner) if partner else None,
        "messages": messages
    }

@app.post("/api/dms/{other_user_id}")
async def send_direct_message(other_user_id: int, req: DirectMessageRequest, user: dict = Depends(get_current_user)):
    clean_msg = req.message.strip()
    if not clean_msg:
        raise HTTPException(status_code=400, detail="Message cannot be empty")
    
    if user["id"] == other_user_id:
        raise HTTPException(status_code=400, detail="Cannot message yourself")

    with get_db_cursor(commit=True) as cur:
        cur.execute("SELECT id FROM users WHERE id = ?", (other_user_id,))
        if not cur.fetchone():
            raise HTTPException(status_code=404, detail="Recipient not found")

        cur.execute("""
            INSERT INTO direct_messages (sender_id, receiver_id, message, is_read)
            VALUES (?, ?, ?, 0)
        """, (user["id"], other_user_id, clean_msg))
        msg_id = cur.lastrowid

        cur.execute("""
            SELECT dm.*, 
                   s.gamer_tag as sender_tag, s.avatar as sender_avatar,
                   r.gamer_tag as receiver_tag, r.avatar as receiver_avatar
            FROM direct_messages dm
            JOIN users s ON dm.sender_id = s.id
            JOIN users r ON dm.receiver_id = r.id
            WHERE dm.id = ?
        """, (msg_id,))
        msg = dict(cur.fetchone())

    # Send real-time notification to recipient if connected
    await manager.send_user(other_user_id, {
        "type": "new_direct_message",
        "message": msg
    })

    return msg

# --- Friend System ---
@app.get("/api/friends")
def get_friends(user: dict = Depends(get_current_user)):
    with get_db_cursor(commit=False) as cur:
        # Accepted friends
        cur.execute("""
            SELECT u.id, u.username, u.gamer_tag, u.avatar, u.primary_game, u.rank, u.platform, u.is_online, u.karma_score
            FROM friends f
            JOIN users u ON f.friend_id = u.id
            WHERE f.user_id = ? AND f.status = 'accepted'
        """, (user["id"],))
        accepted = [dict(r) for r in cur.fetchall()]

        # Incoming requests
        cur.execute("""
            SELECT f.id as request_id, u.id as user_id, u.username, u.gamer_tag, u.avatar, u.rank, u.primary_game, u.karma_score
            FROM friends f
            JOIN users u ON f.user_id = u.id
            WHERE f.friend_id = ? AND f.status = 'pending'
        """, (user["id"],))
        incoming = [dict(r) for r in cur.fetchall()]

        # Outgoing requests
        cur.execute("""
            SELECT f.id as request_id, u.id as user_id, u.username, u.gamer_tag, u.avatar, u.rank
            FROM friends f
            JOIN users u ON f.friend_id = u.id
            WHERE f.user_id = ? AND f.status = 'pending'
        """, (user["id"],))
        outgoing = [dict(r) for r in cur.fetchall()]

    return {
        "friends": accepted,
        "incoming": incoming,
        "outgoing": outgoing
    }

@app.post("/api/friends/request")
async def send_friend_request(req: FriendActionRequest, user: dict = Depends(get_current_user)):
    target_ident = req.target.strip()
    with get_db_cursor(commit=True) as cur:
        cur.execute("SELECT id, gamer_tag FROM users WHERE username = ? OR gamer_tag = ? COLLATE NOCASE", (target_ident, target_ident))
        target_user = cur.fetchone()
        if not target_user:
            raise HTTPException(status_code=404, detail="Player not found with that GamerTag or username")

        target_id = target_user["id"]
        if target_id == user["id"]:
            raise HTTPException(status_code=400, detail="You cannot add yourself as a friend")

        # Check existing
        cur.execute("SELECT * FROM friends WHERE (user_id = ? AND friend_id = ?) OR (user_id = ? AND friend_id = ?)", (user["id"], target_id, target_id, user["id"]))
        existing = cur.fetchone()
        if existing:
            if existing["status"] == "accepted":
                raise HTTPException(status_code=400, detail="You are already friends with this player")
            else:
                raise HTTPException(status_code=400, detail="Friend request already pending")

        cur.execute("INSERT INTO friends (user_id, friend_id, status) VALUES (?, ?, 'pending')", (user["id"], target_id))

    await manager.send_user(target_id, {
        "type": "incoming_friend_request",
        "sender": {
            "id": user["id"],
            "gamer_tag": user["gamer_tag"],
            "avatar": user["avatar"],
            "rank": user["rank"]
        }
    })

    return {"message": f"Friend request sent to {target_user['gamer_tag']}!"}

@app.post("/api/friends/{requester_id}/accept")
async def accept_friend_request(requester_id: int, user: dict = Depends(get_current_user)):
    with get_db_cursor(commit=True) as cur:
        cur.execute("SELECT * FROM friends WHERE user_id = ? AND friend_id = ? AND status = 'pending'", (requester_id, user["id"]))
        req_row = cur.fetchone()
        if not req_row:
            raise HTTPException(status_code=404, detail="No pending request found")

        # Accept in both directions
        cur.execute("UPDATE friends SET status = 'accepted' WHERE user_id = ? AND friend_id = ?", (requester_id, user["id"]))
        cur.execute("INSERT OR REPLACE INTO friends (user_id, friend_id, status) VALUES (?, ?, 'accepted')", (user["id"], requester_id))

    await manager.send_user(requester_id, {
        "type": "friend_request_accepted",
        "friend": {
            "id": user["id"],
            "gamer_tag": user["gamer_tag"],
            "avatar": user["avatar"]
        }
    })

    return {"message": "Friend request accepted!"}

@app.post("/api/friends/{other_id}/reject")
def reject_or_remove_friend(other_id: int, user: dict = Depends(get_current_user)):
    with get_db_cursor(commit=True) as cur:
        cur.execute("DELETE FROM friends WHERE (user_id = ? AND friend_id = ?) OR (user_id = ? AND friend_id = ?)", (user["id"], other_id, other_id, user["id"]))
    return {"message": "Friend connection removed"}

# --- Gamer Karma & Endorsement System ---
@app.post("/api/users/{target_id}/endorse")
async def endorse_user(target_id: int, req: EndorseRequest, user: dict = Depends(get_current_user)):
    if target_id == user["id"]:
        raise HTTPException(status_code=400, detail="You cannot endorse yourself")

    valid_cats = ["Shotcaller", "Tilt-Proof", "Clutch God", "Good Vibes"]
    if req.category not in valid_cats:
        raise HTTPException(status_code=400, detail="Invalid endorsement category")

    with get_db_cursor(commit=True) as cur:
        cur.execute("SELECT id, gamer_tag FROM users WHERE id = ?", (target_id,))
        target = cur.fetchone()
        if not target:
            raise HTTPException(status_code=404, detail="Player not found")

        cur.execute("""
            INSERT INTO karma_endorsements (from_user_id, to_user_id, category)
            VALUES (?, ?, ?)
        """, (user["id"], target_id, req.category))

        # Increase karma
        cur.execute("UPDATE users SET karma_score = karma_score + 5 WHERE id = ?", (target_id,))
        cur.execute("SELECT karma_score FROM users WHERE id = ?", (target_id,))
        new_karma = cur.fetchone()["karma_score"]

    await manager.send_user(target_id, {
        "type": "endorsement_received",
        "category": req.category,
        "by": user["gamer_tag"],
        "new_karma": new_karma
    })

    return {"message": f"Endorsed {target['gamer_tag']} for '{req.category}' (+5 Karma)!", "karma_score": new_karma}

# --- Gamer Profile & Stats ---
@app.get("/api/users/{user_id}")
def get_user_profile(user_id: int):
    with get_db_cursor(commit=False) as cur:
        cur.execute("SELECT id, username, gamer_tag, country, bio, avatar, primary_game, rank, platform, mic_status, discord_tag, karma_score, is_online, created_at FROM users WHERE id = ?", (user_id,))
        row = cur.fetchone()
        if not row:
            raise HTTPException(status_code=404, detail="Gamer not found")
        
        user_data = dict(row)

        # Endorsements count by category
        cur.execute("""
            SELECT category, count(id) as count
            FROM karma_endorsements
            WHERE to_user_id = ?
            GROUP BY category
        """, (user_id,))
        endorsements = {r["category"]: r["count"] for r in cur.fetchall()}
        user_data["endorsements"] = endorsements

    return user_data

@app.put("/api/users/me")
def update_profile(req: ProfileUpdateRequest, user: dict = Depends(get_current_user)):
    updates = []
    params = []
    for field in ["gamer_tag", "country", "bio", "avatar", "primary_game", "rank", "platform", "mic_status", "discord_tag"]:
        val = getattr(req, field)
        if val is not None:
            updates.append(f"{field} = ?")
            params.append(val.strip() if isinstance(val, str) else val)

    if not updates:
        return user

    params.append(user["id"])
    query = f"UPDATE users SET {', '.join(updates)} WHERE id = ?"
    with get_db_cursor(commit=True) as cur:
        cur.execute(query, params)
        cur.execute("SELECT * FROM users WHERE id = ?", (user["id"],))
        updated = dict(cur.fetchone())
        del updated["password_hash"]

    return updated

@app.get("/api/stats")
def get_platform_stats():
    with get_db_cursor(commit=False) as cur:
        cur.execute("SELECT count(id) as count FROM users")
        total_users = cur.fetchone()["count"]

        cur.execute("SELECT count(id) as count FROM squads WHERE status = 'open'")
        active_squads = cur.fetchone()["count"]

        cur.execute("SELECT count(id) as count FROM chat_messages")
        total_msgs = cur.fetchone()["count"]

    return {
        "online_gamers": max(total_users, 18),
        "active_squads": active_squads,
        "chat_messages": total_msgs,
        "regional_rooms": 15
    }

# --- Gaming Guides & SEO Blog Hub ---
@app.get("/api/blogs")
def list_blogs(category: Optional[str] = None, game: Optional[str] = None, q: Optional[str] = None):
    articles = BLOG_ARTICLES
    if category and category != "All":
        articles = [a for a in articles if a["category"].lower() == category.lower()]
    if game and game != "All Games":
        articles = [a for a in articles if a["game_tag"].lower() == game.lower() or a["game_tag"] == "All Games"]
    if q:
        query = q.lower()
        articles = [a for a in articles if query in a["title"].lower() or query in a["meta_description"].lower() or any(query in k.lower() for k in a["target_keywords"])]

    # Return list without full content_html for bandwidth efficiency
    summary_list = []
    for a in articles:
        summary_list.append({
            "slug": a["slug"],
            "title": a["title"],
            "meta_description": a["meta_description"],
            "category": a["category"],
            "game_tag": a["game_tag"],
            "target_keywords": a["target_keywords"],
            "author": a["author"],
            "published_at": a["published_at"],
            "read_time": a["read_time"],
            "banner_badge": a["banner_badge"],
            "llm_summary": a["llm_summary"]
        })
    return summary_list

@app.get("/api/blogs/{slug}")
def get_blog_article(slug: str):
    article = BLOG_MAP.get(slug)
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
    
    # Also fetch any active squad lobbies matching this game tag
    game_tag = article.get("game_tag")
    matching_squads = []
    if game_tag and game_tag != "All Games":
        with get_db_cursor(commit=False) as cur:
            cur.execute("SELECT s.*, u.gamer_tag as leader_tag, u.avatar as leader_avatar FROM squads s JOIN users u ON s.leader_id = u.id WHERE s.game = ? AND s.status = 'open' LIMIT 3", (game_tag,))
            matching_squads = [dict(r) for r in cur.fetchall()]

    return {
        "article": article,
        "related_squads": matching_squads
    }

# --- WebSockets for Chat, Squads, and DMs ---
@app.websocket("/ws/chat/{room_id}")
async def websocket_chat(websocket: WebSocket, room_id: str):
    room_id = room_id.lower()
    await manager.connect_room(room_id, websocket)
    try:
        while True:
            # We can receive ping/pong or client messages
            data = await websocket.receive_text()
            try:
                payload = json.loads(data)
                # Keepalive / ping
                if payload.get("type") == "ping":
                    await websocket.send_json({"type": "pong"})
            except Exception:
                pass
    except WebSocketDisconnect:
        manager.disconnect_room(room_id, websocket)

@app.websocket("/ws/squad/{squad_id}")
async def websocket_squad(websocket: WebSocket, squad_id: int):
    await manager.connect_squad(squad_id, websocket)
    try:
        while True:
            data = await websocket.receive_text()
            try:
                payload = json.loads(data)
                if payload.get("type") == "ping":
                    await websocket.send_json({"type": "pong"})
            except Exception:
                pass
    except WebSocketDisconnect:
        manager.disconnect_squad(squad_id, websocket)

@app.websocket("/ws/user/{user_id}")
async def websocket_user(websocket: WebSocket, user_id: int):
    await manager.connect_user(user_id, websocket)
    try:
        while True:
            data = await websocket.receive_text()
            try:
                payload = json.loads(data)
                if payload.get("type") == "ping":
                    await websocket.send_json({"type": "pong"})
            except Exception:
                pass
    except WebSocketDisconnect:
        manager.disconnect_user(user_id, websocket)

# --- Mount Static Frontend ---
FRONTEND_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "frontend")
if os.path.exists(FRONTEND_DIR):
    app.mount("/static", StaticFiles(directory=FRONTEND_DIR), name="static")

@app.get("/")
def serve_index():
    index_file = os.path.join(FRONTEND_DIR, "index.html")
    if os.path.exists(index_file):
        return FileResponse(index_file)
    return JSONResponse({"status": "RESPAWN // SQUADFINDER API Running"})
