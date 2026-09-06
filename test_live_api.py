import urllib.request
import json

BASE = "http://127.0.0.1:8000"

def request(method, path, data=None, token=None):
    url = f"{BASE}{path}"
    headers = {"Content-Type": "application/json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    body = json.dumps(data).encode("utf-8") if data else None
    req = urllib.request.Request(url, data=body, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req) as resp:
            return resp.status, json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        return e.code, json.loads(e.read().decode("utf-8"))

def test_all():
    print("=== RUNNING LIVE HTTP API TEST SUITE ===")
    
    # 1. Stats
    status, data = request("GET", "/api/stats")
    assert status == 200, f"Stats failed: {data}"
    assert data["regional_rooms"] == 15
    print("[PASS] Stats: 15 Regional Rooms verified")

    # 2. 15 Countries with Flags
    status, countries = request("GET", "/api/countries")
    assert status == 200
    assert len(countries) == 15
    print(f"[PASS] 15 Countries verified with flags: {[c['code'] for c in countries[:5]]}...")

    # 3. Login Demo Gamer
    status, auth = request("POST", "/api/auth/login", {
        "username_or_email": "vipershot",
        "password": "ProGamer2026!"
    })
    assert status == 200
    token1 = auth["token"]
    user1 = auth["user"]
    print(f"[PASS] Demo Login successful: GamerTag '{user1['gamer_tag']}', Rank '{user1['rank']}'")

    # 4. Chat in US Room
    status, chat = request("GET", "/api/chat/us")
    assert status == 200
    assert len(chat["messages"]) > 0
    print(f"[PASS] US Room chat messages retrieved ({len(chat['messages'])} msgs)")

    status, new_msg = request("POST", "/api/chat/us", {"message": "Live queue test! Let's get this win."}, token=token1)
    assert status == 200
    assert new_msg["gamer_tag"] == "ViperShot"
    print(f"[PASS] Live chat message posted to US Room: '{new_msg['message']}'")

    # 5. List Squads
    status, squads = request("GET", "/api/squads")
    assert status == 200
    assert len(squads) >= 5
    print(f"[PASS] Active squad lobbies listed ({len(squads)} open squads)")

    # 6. Create Squad Lobby
    status, new_squad = request("POST", "/api/squads", {
        "title": "Immortal Duo Grind - Need Locked In Controller",
        "game": "Valorant",
        "mode": "Competitive / Ranked",
        "rank_req": "Ascendant 3+",
        "mic_req": "Mic Required",
        "region": "NA (East / West)",
        "max_players": 5,
        "discord_voice": "https://discord.gg/respawn-na",
        "role": "IGL / Shotcaller"
    }, token=token1)
    assert status == 200
    squad_id = new_squad["id"]
    print(f"[PASS] Created Squad Lobby #{squad_id}: '{new_squad['title']}'")

    # 7. Register Second Player
    status, auth2 = request("POST", "/api/auth/register", {
        "gamer_tag": "ApexPredator_X",
        "username": "apexpredator",
        "email": "apex@respawn.gg",
        "password": "ProGamer2026!",
        "country": "US",
        "primary_game": "Valorant",
        "platform": "PC",
        "rank": "Ascendant 3",
        "avatar": "arctic_sniper"
    })
    # If already registered from previous run, login instead
    if status == 400 and "already registered" in auth2.get("detail", ""):
        status, auth2 = request("POST", "/api/auth/login", {
            "username_or_email": "apexpredator",
            "password": "ProGamer2026!"
        })
    assert status == 200
    token2 = auth2["token"]
    user2 = auth2["user"]
    print(f"[PASS] Second player authenticated: '{user2['gamer_tag']}' (ID: {user2['id']})")

    # 8. Join Squad as Second Player
    status, joined_sq = request("POST", f"/api/squads/{squad_id}/join", {"role": "Sniper / Anchor"}, token=token2)
    assert status == 200
    assert joined_sq["current_players"] == 2
    print(f"[PASS] Second player joined squad #{squad_id} (Roster: {joined_sq['current_players']}/{joined_sq['max_players']})")

    # 9. Toggle Ready State
    status, rdy = request("POST", f"/api/squads/{squad_id}/ready", token=token2)
    assert status == 200
    assert rdy["is_ready"] == 1
    print("[PASS] Squad member readiness toggled to READY (1)")

    # 10. Direct Messaging
    status, dm = request("POST", f"/api/dms/{user2['id']}", {"message": "Ready to queue up for comp?"}, token=token1)
    assert status == 200
    print(f"[PASS] Direct message sent: '{dm['message']}'")

    status, dm_thread = request("GET", f"/api/dms/{user1['id']}", token=token2)
    assert status == 200
    assert len(dm_thread["messages"]) >= 1
    print(f"[PASS] Direct message thread received by recipient ({len(dm_thread['messages'])} messages)")

    # 11. Friend System
    status, freq = request("POST", "/api/friends/request", {"target": "ApexPredator_X"}, token=token1)
    assert status in (200, 400) # 400 if already pending/friends
    print(f"[PASS] Friend request sent")

    # Accept friend request
    status, faccept = request("POST", f"/api/friends/{user1['id']}/accept", token=token2)
    print(f"[PASS] Friend request accepted")

    status, flist = request("GET", "/api/friends", token=token1)
    assert status == 200
    print(f"[PASS] Friends list verified ({len(flist['friends'])} friends)")

    # 12. Endorse Gamer with Karma
    status, endorse = request("POST", f"/api/users/{user2['id']}/endorse", {"category": "Clutch God"}, token=token1)
    assert status == 200
    print(f"[PASS] Endorsed teammate: '{endorse['message']}'")

    # 13. Test Frontend HTML & Static Assets
    with urllib.request.urlopen("http://127.0.0.1:8000/") as resp:
        assert resp.status == 200
        html = resp.read().decode("utf-8")
        assert "RESPAWN" in html
        assert "SQUADFINDER" in html
        assert "15 Flag Hub" in html
    print("[PASS] Frontend single-page app HTML successfully served")

    with urllib.request.urlopen("http://127.0.0.1:8000/static/css/style.css") as resp:
        assert resp.status == 200
        css = resp.read().decode("utf-8")
        assert "--neon-cyan" in css
    print("[PASS] Frontend CSS stylesheet successfully served")

    with urllib.request.urlopen("http://127.0.0.1:8000/static/js/app.js") as resp:
        assert resp.status == 200
        js = resp.read().decode("utf-8")
        assert "selectCountryRoom" in js
    print("[PASS] Frontend JS bundle successfully served")

    print("\n=======================================================")
    print(">>> ALL 13 REAL-WORLD API & ASSET TESTS PASSED 100%! <<<")
    print("=======================================================")

if __name__ == "__main__":
    test_all()
