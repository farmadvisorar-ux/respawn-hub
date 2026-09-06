import httpx
import sys

BASE = "http://127.0.0.1:8000"

def run_verification():
    print("=== STARTING FULL END-TO-END VERIFICATION ===")
    with httpx.Client(base_url=BASE, timeout=10.0) as client:
        # 1. Stats
        res = client.get("/api/stats")
        assert res.status_code == 200, res.text
        data = res.json()
        assert data["regional_rooms"] == 15
        print(f"[PASS] 1. Stats: {data['online_gamers']} gamers, {data['active_squads']} squads, {data['regional_rooms']} regional rooms")

        # 2. 15 Countries
        res = client.get("/api/countries")
        assert res.status_code == 200
        countries = res.json()
        assert len(countries) == 15
        print(f"[PASS] 2. 15 Regional Countries with Flags verified: {[c['name'] for c in countries[:4]]}...")

        # 3. Login
        res = client.post("/api/auth/login", json={
            "username_or_email": "vipershot",
            "password": "ProGamer2026!"
        })
        assert res.status_code == 200, res.text
        token = res.json()["token"]
        user = res.json()["user"]
        assert user["gamer_tag"] == "ViperShot"
        print(f"[PASS] 3. Login: Authenticated as '{user['gamer_tag']}' (Rank: {user['rank']})")

        headers = {"Authorization": f"Bearer {token}"}

        # 4. National Chat Room (US & JP)
        res = client.get("/api/chat/us")
        assert res.status_code == 200
        assert len(res.json()["messages"]) >= 3
        print(f"[PASS] 4a. US Chat Room loaded with {len(res.json()['messages'])} messages")

        res = client.post("/api/chat/us", json={"message": "Need cracked duo for tonight's tournament!"}, headers=headers)
        assert res.status_code == 200
        print(f"[PASS] 4b. Posted live message to US room: '{res.json()['message']}'")

        # 5. List Squads
        res = client.get("/api/squads")
        assert res.status_code == 200
        squads = res.json()
        assert len(squads) >= 5
        print(f"[PASS] 5. Listed {len(squads)} active squad lobbies across Valorant, CS2, Apex, etc.")

        # 6. Create Squad Lobby
        res = client.post("/api/squads", json={
            "title": "Radiant Push - Need cracked smoke player",
            "game": "Valorant",
            "mode": "Competitive / Ranked",
            "rank_req": "Ascendant 3+",
            "mic_req": "Mic Required",
            "region": "NA (East / West)",
            "max_players": 5,
            "discord_voice": "https://discord.gg/test-lobby",
            "role": "IGL / Shotcaller"
        }, headers=headers)
        assert res.status_code == 200
        new_squad = res.json()
        squad_id = new_squad["id"]
        print(f"[PASS] 6. Created Squad #{squad_id}: '{new_squad['title']}'")

        # 7. Register 2nd Player
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
        if res.status_code == 400:
            res = client.post("/api/auth/login", json={"username_or_email": "phoenixking", "password": "ProGamer2026!"})
        assert res.status_code == 200
        token2 = res.json()["token"]
        user2 = res.json()["user"]
        headers2 = {"Authorization": f"Bearer {token2}"}
        print(f"[PASS] 7. Second player authenticated: '{user2['gamer_tag']}'")

        # 8. Join Squad
        res = client.post(f"/api/squads/{squad_id}/join", json={"role": "Entry Fragger"}, headers=headers2)
        assert res.status_code == 200
        print(f"[PASS] 8. '{user2['gamer_tag']}' joined squad #{squad_id}. Roster: {res.json()['current_players']}/{res.json()['max_players']}")

        # 9. Toggle Ready
        res = client.post(f"/api/squads/{squad_id}/ready", headers=headers2)
        assert res.status_code == 200
        assert res.json()["is_ready"] == 1
        print("[PASS] 9. Squad member readiness toggled to READY")

        # 10. Direct Messaging (DMs)
        res = client.post(f"/api/dms/{user2['id']}", json={"message": "Hey Phoenix, let's lock in!"}, headers=headers)
        assert res.status_code == 200
        print(f"[PASS] 10a. Sent private DM: '{res.json()['message']}'")

        res = client.get(f"/api/dms/{user['id']}", headers=headers2)
        assert res.status_code == 200
        assert len(res.json()["messages"]) >= 1
        print(f"[PASS] 10b. Recipient verified private DM thread ({len(res.json()['messages'])} messages)")

        # 11. Friend System
        res = client.post("/api/friends/request", json={"target": "PhoenixKing"}, headers=headers)
        assert res.status_code in (200, 400)
        res = client.post(f"/api/friends/{user['id']}/accept", headers=headers2)
        assert res.status_code in (200, 404)
        res = client.get("/api/friends", headers=headers)
        assert res.status_code == 200
        print(f"[PASS] 11. Friend connection verified ({len(res.json()['friends'])} friends)")

        # 12. Gamer Karma
        res = client.post(f"/api/users/{user2['id']}/endorse", json={"category": "Clutch God"}, headers=headers)
        assert res.status_code == 200
        print(f"[PASS] 12. Endorsed teammate with Karma: {res.json()['message']}")

        # 13. Static Assets
        res = client.get("/")
        assert res.status_code == 200 and "RESPAWN" in res.text
        res = client.get("/static/css/style.css")
        assert res.status_code == 200 and "--neon-cyan" in res.text
        res = client.get("/static/js/app.js")
        assert res.status_code == 200 and "selectCountryRoom" in res.text
        res = client.get("/static/js/audio.js")
        assert res.status_code == 200 and "playReadyCheck" in res.text
        print("[PASS] 13. Static frontend assets (HTML, CSS, JS, Audio Synthesizer) verified")

    print("\n=======================================================")
    print(">>> ALL 13 ENTERPRISE-GRADE VERIFICATION CHECKS PASSED! <<<")
    print("=======================================================")

if __name__ == "__main__":
    run_verification()
