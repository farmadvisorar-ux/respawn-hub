import urllib.request
import urllib.parse
import json
import sys

BASE_URL = "http://127.0.0.1:8000"

def get(path):
    url = f"{BASE_URL}{path}"
    req = urllib.request.Request(url)
    with urllib.request.urlopen(req, timeout=10) as resp:
        return resp.status, json.loads(resp.read().decode("utf-8"))

def test_blogs_list():
    print(">>> Testing GET /api/blogs...")
    status, blogs = get("/api/blogs")
    assert status == 200, f"Expected 200, got {status}"
    assert len(blogs) >= 5, f"Expected at least 5 articles, got {len(blogs)}"
    print(f"    Found {len(blogs)} articles:")
    for b in blogs:
        print(f"    - [{b['category']}] {b['title'][:60]}... ({b['read_time']})")
    return blogs

def test_blogs_filtering():
    print(">>> Testing blog categories & search filters...")
    status, top10 = get("/api/blogs?category=Top%2010")
    assert status == 200
    assert len(top10) >= 2, f"Expected at least 2 Top 10 articles, got {len(top10)}"
    print(f"    Top 10 filter count: {len(top10)}")

    status, mc = get("/api/blogs?game=Minecraft")
    assert status == 200
    assert any("Minecraft" in b["title"] for b in mc), "Minecraft article not found in game filter"
    print(f"    Minecraft filter count: {len(mc)}")

    status, searched = get("/api/blogs?q=resurgence")
    assert status == 200
    assert len(searched) >= 1, "Warzone search for 'resurgence' failed"
    print(f"    Search query 'resurgence' matched: {searched[0]['title'][:50]}")

def test_single_article(slug):
    print(f">>> Testing GET /api/blogs/{slug}...")
    status, data = get(f"/api/blogs/{slug}")
    assert status == 200
    art = data.get("article", data)
    assert "content_html" in art
    assert "schema_data" in art
    assert art["schema_data"]["@type"] == "BlogPosting"
    assert "llm_summary" in art
    print(f"    Loaded: {art['title'][:50]}... | Schema: {art['schema_data']['headline'][:40]}...")

def test_squads_new_games():
    print(">>> Testing squads with new games (Fortnite, Minecraft, Roblox, Call of Duty)...")
    status, squads = get("/api/squads")
    assert status == 200
    games = {s["game"] for s in squads}
    print(f"    Games currently with active squads: {games}")

    target_games = ["Fortnite", "Minecraft", "Roblox", "Call of Duty"]
    for tg in target_games:
        status, filtered = get(f"/api/squads?game={urllib.parse.quote(tg)}")
        assert status == 200
        print(f"    Squads for {tg}: {len(filtered)}")

def main():
    try:
        blogs = test_blogs_list()
        test_blogs_filtering()
        for b in blogs:
            test_single_article(b["slug"])
        test_squads_new_games()
        print("\n[PASS] All blog and game verification tests succeeded flawlessly!")
    except Exception as e:
        print(f"\n[FAIL] Verification error: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
