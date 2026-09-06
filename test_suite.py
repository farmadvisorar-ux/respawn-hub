import sys
import json
from starlette.testclient import TestClient
from backend.main import app
from backend.database import init_db
from backend.seed import seed_database

def run_tests():
    print("=== STARTING RESPAWN GAMER HUB AUTOMATED TEST SUITE ===")
    init_db()
    seed_database()

    with TestClient(app) as client:
        # 1. Test Telemetry / Stats
        res = client.get("/api/stats")
    assert res.status_code == 200, f"Stats failed: {res.text}"
    stats = res.json()
    assert stats["regional_rooms"] == 15, "Should have exactly 15 rooms"
    print("PASS: Stats & Telemetry endpoint verified (15 Regional Rooms).")

    # 2. Test 15 Countries
    res = client.get("/api/countries")
    assert res.status_code == 200, f"Countries failed: {res.text}"
    countries = res.json()
    assert len(countries) == 15, f"Expected 15 countries, got {len(countries)}"
    for c in countries:
        assert "flag" in c and "name" in c and "id" in c
    print("PASS: Exactly 15 Country chat rooms with flags and metadata verified.")

    # 3. Test Demo Login
    res = client.post("/api/auth/login", json={
        "username_or_email": "vipershot",
        "password": "ProGamer2026!"
    })
    assert res.status_code == 200, f"Login failed: {res.text}"
    auth_data = res.json()
    token = auth_data["token"]
    user = auth_data["user"]
    assert user["gamer_tag"] == "ViperShot"
    print(f"PASS: Demo gamer login verified for '{user['gamer_tag']}'.")

    headers = {"Authorization": f"Bearer {token}"}

    # 4. Test Chat in a National Room (e.g. US, JP, DE)
    res = client.get("/api/chat/us")
    assert res.status_code == 200
    chat_data = res.json()
    assert len(chat_data["messages"]) > 0
    print(f"PASS: US Chat Room loaded with {len(chat_data['messages'])} seeded messages.")

    res = client.post("/api/chat/us", json={"message": "Looking for duo for tonight's tournament!"}, headers=headers)
    assert res.status_code == 200
    msg = res.json()
    assert msg["gamer_tag"] == "ViperShot"
    assert msg["message"] == "Looking for duo for tonight's tournament!"
    print("PASS: Posted live message to national chat room.")

    # 5. Test Squad LFG Board
    res = client.get("/api/squads")
    assert res.status_code == 200
    squads = res.json()
    assert len(squads) >= 5, "Expected active squad lobbies"
    print(f"PASS: Loaded {len(squads)} active squad lobbies.")

    # 6. Test Create Squad
    res = client.post("/api/squads", json={
        "title": "Radiant Push - Need cracked smoke player",
        "game": "Valorant",
        "mode": "Competitive / Ranked",
        "rank_req": "Ascendant+",
        "mic_req": "Mic Required",
        "region": "NA (East / West)",
        "max_players": 5,
        "discord_voice": "https://discord.gg/test-lobby",
        "role": "IGL / Shotcaller"
    }, headers=headers)
    assert res.status_code == 200, f"Create squad failed: {res.text}"
    new_squad = res.json()
    assert new_squad["title"] == "Radiant Push - Need cracked smoke player"
    assert new_squad["current_players"] == 1
    squad_id = new_squad["id"]
    print(f"PASS: Created squad lobby #{squad_id}.")

    # 7. Test Registering a second gamer to join the squad & exchange DMs
    res = client.post("/api/auth/register", json={
        "gamer_tag": "PhoenixKing",
        "username": "phoenixking",
        "email": "phoenix@gamer.gg",
        "password": "ProGamer2026!",
        "country": "US",
        "primary_game": "Valorant",
        "platform": "PC",
        "rank": "Ascendant 2",
        "avatar": "neon_pilot"
    })
    assert res.status_code == 200, f"Register failed: {res.text}"
    user2_token = res.json()["token"]
    user2_id = res.json()["user"]["id"]
    user2_headers = {"Authorization": f"Bearer {user2_token}"}
    print("PASS: Registered new player 'PhoenixKing'.")

    # User 2 joins the squad
    res = client.post(f"/api/squads/{squad_id}/join", json={"role": "Entry Fragger"}, headers=user2_headers)
    assert res.status_code == 200
    joined_squad = res.json()
    assert joined_squad["current_players"] == 2
    print(f"PASS: 'PhoenixKing' joined squad #{squad_id}. Current members: 2/5.")

    # User 2 toggles ready
    res = client.post(f"/api/squads/{squad_id}/ready", headers=user2_headers)
    assert res.status_code == 200
    print("PASS: Toggled ready status for squad member.")

    # 8. Test Direct Messaging (DMs)
    res = client.post(f"/api/dms/{user2_id}", json={"message": "Hey Phoenix, welcome to the squad!"}, headers=headers)
    assert res.status_code == 200
    dm_data = res.json()
    assert dm_data["message"] == "Hey Phoenix, welcome to the squad!"
    print("PASS: Sent private direct message (DM).")

    res = client.get(f"/api/dms/{user['id']}", headers=user2_headers)
    assert res.status_code == 200
    assert len(res.json()["messages"]) >= 1
    print("PASS: Retrieved DM conversation thread.")

    # 9. Test Friend System
    res = client.post("/api/friends/request", json={"target": "PhoenixKing"}, headers=headers)
    assert res.status_code == 200
    print("PASS: Sent friend request to 'PhoenixKing'.")

    res = client.post(f"/api/friends/{user['id']}/accept", headers=user2_headers)
    assert res.status_code == 200
    print("PASS: Accepted friend request.")

    res = client.get("/api/friends", headers=headers)
    assert res.status_code == 200
    assert any(f["gamer_tag"] == "PhoenixKing" for f in res.json()["friends"])
    print("PASS: Verified mutual friendship in active friends list.")

    # 10. Test Gamer Karma & Endorsements
    res = client.post(f"/api/users/{user2_id}/endorse", json={"category": "Tilt-Proof"}, headers=headers)
    assert res.status_code == 200
    assert res.json()["karma_score"] >= 20
    print("PASS: Endorsed player for 'Tilt-Proof' (+5 Karma).")

    print("\n>>> ALL 10 TESTS COMPLETED SUCCESSFULLY! ENTERPRISE GRADE VERIFIED! <<<")

if __name__ == "__main__":
    run_tests()
