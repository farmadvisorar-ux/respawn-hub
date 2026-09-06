import urllib.request
import urllib.parse
import json
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

BASE_URL = "http://127.0.0.1:8000"

def get(path):
    url = f"{BASE_URL}{path}"
    req = urllib.request.Request(url)
    with urllib.request.urlopen(req, timeout=10) as resp:
        return resp.status, json.loads(resp.read().decode("utf-8"))

def test_countries_api():
    print(">>> Testing GET /api/countries...")
    status, rooms = get("/api/countries")
    assert status == 200
    assert len(rooms) >= 22, f"Expected 22 rooms, got {len(rooms)}"
    
    national_rooms = [r for r in rooms if r.get("category") == "national"]
    other_rooms = [r for r in rooms if r.get("category") == "other_language"]
    assert len(national_rooms) == 15, f"Expected 15 national rooms, got {len(national_rooms)}"
    assert len(other_rooms) >= 7, f"Expected at least 7 other language rooms, got {len(other_rooms)}"
    
    print(f"    Total rooms: {len(rooms)}")
    print(f"    15 National Hubs:")
    for r in national_rooms:
        assert "language" in r and "quick_phrases" in r, f"Missing language or quick phrases in {r['name']}"
        print(f"    - {r['flag']} {r['name']} | Lang: {r['language']} | Phrases: {len(r['quick_phrases'])}")

    print(f"    Other Language Hubs:")
    for r in other_rooms:
        assert "language" in r and "quick_phrases" in r, f"Missing language or quick phrases in {r['name']}"
        print(f"    - {r['flag']} {r['name']} | Lang: {r['language']} | Phrases: {len(r['quick_phrases'])}")

def test_language_filtering():
    print(">>> Testing language filtering on /api/countries...")
    status, national = get("/api/countries?category=national")
    assert status == 200 and len(national) == 15

    status, others = get("/api/countries?category=other_language")
    assert status == 200 and len(others) == 7

    status, ja = get("/api/countries?language=" + urllib.parse.quote("日本語"))
    assert status == 200 and any(r["id"] == "jp" for r in ja)
    print(f"    Japanese filter matched: {[r['name'] for r in ja]}")

    status, de = get("/api/countries?language=" + urllib.parse.quote("Deutsch"))
    assert status == 200 and any(r["id"] == "de" for r in de)
    print(f"    German filter matched: {[r['name'] for r in de]}")

    status, es = get("/api/countries?language=" + urllib.parse.quote("Español"))
    assert status == 200 and len(es) >= 2 # Spain + Mexico
    print(f"    Spanish filter matched: {[r['name'] for r in es]}")

def test_room_messages():
    print(">>> Testing native language messages in various rooms...")
    test_rooms = ["jp", "kr", "de", "fr", "br", "es", "cn", "mena", "tr", "vn", "in", "global"]
    for rid in test_rooms:
        status, data = get(f"/api/chat/{rid}")
        assert status == 200, f"Failed to get messages for {rid}"
        messages = data.get("messages", [])
        assert len(messages) >= 3, f"Expected at least 3 messages in {rid}, got {len(messages)}"
        print(f"    Room [{rid.upper()}]: {len(messages)} messages loaded successfully.")

def main():
    try:
        test_countries_api()
        test_language_filtering()
        test_room_messages()
        print("\n[PASS] All 15 National Hubs + World Language Chat Rooms verified successfully!")
    except Exception as e:
        print(f"\n[FAIL] Verification error: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
