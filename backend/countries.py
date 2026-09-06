# 15 Regional Country Chat Rooms with National Flags and Regional Metadata

COUNTRIES = [
    {
        "id": "us",
        "code": "US",
        "name": "United States",
        "flag": "🇺🇸",
        "region": "NA (East / West)",
        "hub": "Ashburn / Silicon Valley",
        "popular_games": ["Valorant", "Fortnite", "Call of Duty", "Roblox", "Minecraft"],
        "tagline": "NA Ranked Grind & College Esports"
    },
    {
        "id": "gb",
        "code": "GB",
        "name": "United Kingdom",
        "flag": "🇬🇧",
        "region": "EU West",
        "hub": "London",
        "popular_games": ["CS2", "Fortnite", "Call of Duty", "Minecraft", "Rocket League"],
        "tagline": "UK LFG & Competitive Ladders"
    },
    {
        "id": "ca",
        "code": "CA",
        "name": "Canada",
        "flag": "🇨🇦",
        "region": "NA North",
        "hub": "Montreal / Toronto / Vancouver",
        "popular_games": ["Valorant", "Call of Duty", "Minecraft", "Apex Legends", "Fortnite"],
        "tagline": "Chill Vibes & Competitive Scrims"
    },
    {
        "id": "de",
        "code": "DE",
        "name": "Germany",
        "flag": "🇩🇪",
        "region": "EU Central",
        "hub": "Frankfurt",
        "popular_games": ["CS2", "Minecraft", "Rainbow Six Siege", "Valorant", "Fortnite"],
        "tagline": "DACH Esports & Tactical Squads"
    },
    {
        "id": "fr",
        "code": "FR",
        "name": "France",
        "flag": "🇫🇷",
        "region": "EU West",
        "hub": "Paris",
        "popular_games": ["Valorant", "Rocket League", "League of Legends", "CS2"],
        "tagline": "LFL Energy & High-Elo Stacks"
    },
    {
        "id": "jp",
        "code": "JP",
        "name": "Japan",
        "flag": "🇯🇵",
        "region": "Asia-Pacific",
        "hub": "Tokyo",
        "popular_games": ["Apex Legends", "Valorant", "Street Fighter 6", "Overwatch 2"],
        "tagline": "Tokyo Apex Grinders & Tactical VCT"
    },
    {
        "id": "kr",
        "code": "KR",
        "name": "South Korea",
        "flag": "🇰🇷",
        "region": "East Asia",
        "hub": "Seoul",
        "popular_games": ["League of Legends", "Overwatch 2", "Valorant", "PUBG"],
        "tagline": "PC Bang Culture & World Champions"
    },
    {
        "id": "br",
        "code": "BR",
        "name": "Brazil",
        "flag": "🇧🇷",
        "region": "South America",
        "hub": "São Paulo",
        "popular_games": ["CS2", "Valorant", "League of Legends", "Free Fire"],
        "tagline": "Major Passion & Aggressive Entry Play"
    },
    {
        "id": "au",
        "code": "AU",
        "name": "Australia",
        "flag": "🇦🇺",
        "region": "Oceania",
        "hub": "Sydney / Melbourne",
        "popular_games": ["Valorant", "CS2", "Apex Legends", "Dota 2"],
        "tagline": "OCE Banter & Late Night Queues"
    },
    {
        "id": "se",
        "code": "SE",
        "name": "Sweden",
        "flag": "🇸🇪",
        "region": "Nordics",
        "hub": "Stockholm",
        "popular_games": ["CS2", "Dota 2", "Valorant", "Rocket League"],
        "tagline": "Counter-Strike Heritage & Elite Aims"
    },
    {
        "id": "pl",
        "code": "PL",
        "name": "Poland",
        "flag": "🇵🇱",
        "region": "EU East",
        "hub": "Warsaw / Katowice",
        "popular_games": ["CS2", "League of Legends", "Valorant", "Dota 2"],
        "tagline": "Katowice Spodek Spirit & Clutch Players"
    },
    {
        "id": "es",
        "code": "ES",
        "name": "Spain",
        "flag": "🇪🇸",
        "region": "EU South",
        "hub": "Madrid / Barcelona",
        "popular_games": ["Valorant", "League of Legends", "EA FC", "Fortnite"],
        "tagline": "Superliga Passion & High Intensity"
    },
    {
        "id": "it",
        "code": "IT",
        "name": "Italy",
        "flag": "🇮🇹",
        "region": "EU South",
        "hub": "Milan / Rome",
        "popular_games": ["Valorant", "Rainbow Six Siege", "EA FC", "CS2"],
        "tagline": "Italian Gaming Community & Ranked Stacks"
    },
    {
        "id": "mx",
        "code": "MX",
        "name": "Mexico",
        "flag": "🇲🇽",
        "region": "Latin America North",
        "hub": "Mexico City / Monterrey",
        "popular_games": ["Valorant", "League of Legends", "Warzone", "Halo"],
        "tagline": "LATAM North Community & Squad LFG"
    },
    {
        "id": "nl",
        "code": "NL",
        "name": "Netherlands",
        "flag": "🇳🇱",
        "region": "EU West",
        "hub": "Amsterdam",
        "popular_games": ["Rocket League", "Valorant", "League of Legends", "CS2"],
        "tagline": "Ultra-Low Ping & Tactical Comms"
    }
]

COUNTRY_MAP = {c["id"]: c for c in COUNTRIES}
