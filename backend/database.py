import sqlite3
import os
import threading
from contextlib import contextmanager

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "respawn.db")
_lock = threading.RLock()

def get_db():
    conn = sqlite3.connect(DB_PATH, timeout=20.0, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

@contextmanager
def get_db_cursor(commit=True):
    with _lock:
        conn = get_db()
        try:
            cursor = conn.cursor()
            yield cursor
            if commit:
                conn.commit()
        finally:
            conn.close()

def init_db():
    with get_db_cursor(commit=True) as cur:
        cur.execute("PRAGMA journal_mode=WAL;")
        cur.execute("PRAGMA synchronous=NORMAL;")
        # Users
        cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            gamer_tag TEXT NOT NULL,
            country TEXT DEFAULT 'US',
            bio TEXT DEFAULT '',
            avatar TEXT DEFAULT 'cyber_ninja',
            primary_game TEXT DEFAULT 'Valorant',
            rank TEXT DEFAULT 'Diamond',
            platform TEXT DEFAULT 'PC',
            mic_status TEXT DEFAULT 'Always On',
            discord_tag TEXT DEFAULT '',
            karma_score INTEGER DEFAULT 15,
            is_online INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)

        # Country Chat Rooms (15 nations)
        cur.execute("""
        CREATE TABLE IF NOT EXISTS chat_messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            room_id TEXT NOT NULL,
            user_id INTEGER NOT NULL,
            gamer_tag TEXT NOT NULL,
            avatar TEXT NOT NULL,
            rank TEXT NOT NULL,
            country TEXT NOT NULL,
            message TEXT NOT NULL,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
        """)

        # Direct Messages
        cur.execute("""
        CREATE TABLE IF NOT EXISTS direct_messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sender_id INTEGER NOT NULL,
            receiver_id INTEGER NOT NULL,
            message TEXT NOT NULL,
            is_read INTEGER DEFAULT 0,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(sender_id) REFERENCES users(id),
            FOREIGN KEY(receiver_id) REFERENCES users(id)
        )
        """)

        # Friends
        cur.execute("""
        CREATE TABLE IF NOT EXISTS friends (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            friend_id INTEGER NOT NULL,
            status TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(user_id, friend_id),
            FOREIGN KEY(user_id) REFERENCES users(id),
            FOREIGN KEY(friend_id) REFERENCES users(id)
        )
        """)

        # Squads / LFG Lobbies
        cur.execute("""
        CREATE TABLE IF NOT EXISTS squads (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            leader_id INTEGER NOT NULL,
            title TEXT NOT NULL,
            game TEXT NOT NULL,
            mode TEXT NOT NULL,
            rank_req TEXT NOT NULL,
            mic_req TEXT NOT NULL,
            region TEXT NOT NULL,
            max_players INTEGER DEFAULT 5,
            discord_voice TEXT DEFAULT '',
            status TEXT DEFAULT 'open',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(leader_id) REFERENCES users(id)
        )
        """)

        # Squad Members
        cur.execute("""
        CREATE TABLE IF NOT EXISTS squad_members (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            squad_id INTEGER NOT NULL,
            user_id INTEGER NOT NULL,
            role TEXT DEFAULT 'Flex',
            is_ready INTEGER DEFAULT 0,
            joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(squad_id, user_id),
            FOREIGN KEY(squad_id) REFERENCES squads(id) ON DELETE CASCADE,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
        """)

        # Karma Endorsements
        cur.execute("""
        CREATE TABLE IF NOT EXISTS karma_endorsements (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            from_user_id INTEGER NOT NULL,
            to_user_id INTEGER NOT NULL,
            category TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(from_user_id) REFERENCES users(id),
            FOREIGN KEY(to_user_id) REFERENCES users(id)
        )
        """)

        # Session Tokens
        cur.execute("""
        CREATE TABLE IF NOT EXISTS sessions (
            token TEXT PRIMARY KEY,
            user_id INTEGER NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
        """)
        
        # Indexes for fast querying
        cur.execute("CREATE INDEX IF NOT EXISTS idx_chat_room ON chat_messages(room_id, timestamp)")
        cur.execute("CREATE INDEX IF NOT EXISTS idx_dm_users ON direct_messages(sender_id, receiver_id)")
        cur.execute("CREATE INDEX IF NOT EXISTS idx_squad_game ON squads(game, status)")
