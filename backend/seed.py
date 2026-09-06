import random
from backend.database import get_db_cursor
from backend.auth import hash_password
from backend.countries import COUNTRIES

SAMPLE_USERS = [
    {
        "username": "vipershot",
        "gamer_tag": "ViperShot",
        "email": "viper@respawn.gg",
        "country": "US",
        "avatar": "cyber_ninja",
        "primary_game": "Valorant",
        "rank": "Ascendant 3",
        "platform": "PC",
        "mic_status": "Always On",
        "bio": "Initiator/Controller main. 144Hz setup. Looking for chill but locked-in duo/trio to hit Immortal.",
        "discord_tag": "vipershot#0001",
        "karma_score": 48
    },
    {
        "username": "neonvalkyrie",
        "gamer_tag": "NeonValkyrie",
        "email": "valk@respawn.gg",
        "country": "GB",
        "avatar": "neon_pilot",
        "primary_game": "Apex Legends",
        "rank": "Master",
        "platform": "PC",
        "mic_status": "Push to Talk",
        "bio": "Horizon / Conduit main. Fast rotation shotcalling. No tilt, good vibes only.",
        "discord_tag": "valkyrie_eu",
        "karma_score": 62
    },
    {
        "username": "shadowstriker",
        "gamer_tag": "ShadowStriker",
        "email": "shadow@respawn.gg",
        "country": "DE",
        "avatar": "tactical_ghost",
        "primary_game": "CS2",
        "rank": "Faceit Lvl 9",
        "platform": "PC",
        "mic_status": "Always On",
        "bio": "Entry fragger & secondary AWPer. Frankfurt server low ping. LF 5-stack for weekend premier grind.",
        "discord_tag": "shadow_de",
        "karma_score": 39
    },
    {
        "username": "kabora",
        "gamer_tag": "Kabora_KR",
        "email": "kabora@respawn.gg",
        "country": "KR",
        "avatar": "mech_warrior",
        "primary_game": "League of Legends",
        "rank": "Grandmaster",
        "platform": "PC",
        "mic_status": "Always On",
        "bio": "Mid lane assassin / control mage pool. Looking for aggressive jungle duo to climb.",
        "discord_tag": "kabora_kr",
        "karma_score": 85
    },
    {
        "username": "sakurablade",
        "gamer_tag": "SakuraBlade",
        "email": "sakura@respawn.gg",
        "country": "JP",
        "avatar": "cyber_samurai",
        "primary_game": "Valorant",
        "rank": "Immortal 1",
        "platform": "PC",
        "mic_status": "Always On",
        "bio": "Duelist Jett/Reyna main. Tokyo/Seoul servers. Let's aim high together!",
        "discord_tag": "sakura_jp",
        "karma_score": 54
    },
    {
        "username": "furioustactics",
        "gamer_tag": "FuriousBR",
        "email": "furious@respawn.gg",
        "country": "BR",
        "avatar": "bionic_brawler",
        "primary_game": "CS2",
        "rank": "Global Elite",
        "platform": "PC",
        "mic_status": "Always On",
        "bio": "Bora jogar sério! IGL shotcaller, mira afiada. Looking for high level comp squad.",
        "discord_tag": "furious_br",
        "karma_score": 41
    },
    {
        "username": "frostbite_ca",
        "gamer_tag": "FrostBite",
        "email": "frost@respawn.gg",
        "country": "CA",
        "avatar": "arctic_sniper",
        "primary_game": "Warzone",
        "rank": "Crimson",
        "platform": "PS5",
        "mic_status": "Always On",
        "bio": "Rebirth Island & Urzikstan sweeper. Callouts on point, let's grab some wins.",
        "discord_tag": "frostbite#7777",
        "karma_score": 33
    },
    {
        "username": "aussieaimer",
        "gamer_tag": "AussieAimer",
        "email": "aussie@respawn.gg",
        "country": "AU",
        "avatar": "cyber_ninja",
        "primary_game": "Overwatch 2",
        "rank": "Master 4",
        "platform": "PC",
        "mic_status": "Always On",
        "bio": "Hitscan DPS / Ana main. Late night OCE queues. Positive vibes, zero toxicity.",
        "discord_tag": "aussie_aimer",
        "karma_score": 50
    },
    {
        "username": "nordicviking",
        "gamer_tag": "NordicGhost",
        "email": "nordic@respawn.gg",
        "country": "SE",
        "avatar": "tactical_ghost",
        "primary_game": "CS2",
        "rank": "Faceit Lvl 10",
        "platform": "PC",
        "mic_status": "Always On",
        "bio": "Stockholm servers. Calm comms, precise utility line-ups. Looking for serious team practice.",
        "discord_tag": "nordic_cs",
        "karma_score": 78
    },
    {
        "username": "pixelphoenix",
        "gamer_tag": "PixelPhoenix",
        "email": "pixel@respawn.gg",
        "country": "FR",
        "avatar": "neon_pilot",
        "primary_game": "Rocket League",
        "rank": "Grand Champion I",
        "platform": "PC",
        "mic_status": "Push to Talk",
        "bio": "Rotations & aerial passing play. Looking for consistent 2s or 3s partner.",
        "discord_tag": "pixel_fr",
        "karma_score": 29
    },
    {
        "username": "hussar_aim",
        "gamer_tag": "HussarPL",
        "email": "hussar@respawn.gg",
        "country": "PL",
        "avatar": "mech_warrior",
        "primary_game": "Dota 2",
        "rank": "Divine 3",
        "platform": "PC",
        "mic_status": "Always On",
        "bio": "Pos 1/2 carry. Warsaw ping. Competitive tryhard, ready to communicate and win.",
        "discord_tag": "hussar_pl",
        "karma_score": 36
    },
    {
        "username": "matador_es",
        "gamer_tag": "MatadorES",
        "email": "matador@respawn.gg",
        "country": "ES",
        "avatar": "bionic_brawler",
        "primary_game": "Valorant",
        "rank": "Diamond 2",
        "platform": "PC",
        "mic_status": "Always On",
        "bio": "Sova/Fade recon master. Buenas comunicaciones y ganas de subir a Ascendant.",
        "discord_tag": "matador_es",
        "karma_score": 27
    },
    {
        "username": "gladiatore",
        "gamer_tag": "GladiatoreIT",
        "email": "gladiator@respawn.gg",
        "country": "IT",
        "avatar": "cyber_samurai",
        "primary_game": "Rainbow Six Siege",
        "rank": "Emerald 1",
        "platform": "Xbox",
        "mic_status": "Always On",
        "bio": "Anchor / roam denier. Milan ping 12ms. Cerco compagni per ranked serie.",
        "discord_tag": "gladiatore_it",
        "karma_score": 24
    },
    {
        "username": "azteca_warrior",
        "gamer_tag": "AztecaMX",
        "email": "azteca@respawn.gg",
        "country": "MX",
        "avatar": "arctic_sniper",
        "primary_game": "Warzone",
        "rank": "Diamond 3",
        "platform": "PC",
        "mic_status": "Always On",
        "bio": "Sniper / flanker. Buscando squad para Resurgimiento y Ranked. Buenas vibras!",
        "discord_tag": "azteca_mx",
        "karma_score": 31
    },
    {
        "username": "orange_flash",
        "gamer_tag": "OrangeFlashNL",
        "email": "orange@respawn.gg",
        "country": "NL",
        "avatar": "neon_pilot",
        "primary_game": "Valorant",
        "rank": "Immortal 2",
        "platform": "PC",
        "mic_status": "Always On",
        "bio": "Smoke player Omen/Astra. Amsterdam server 5ms ping. Let's execute clean rounds.",
        "discord_tag": "orange_nl",
        "karma_score": 58
    }
]

COUNTRY_CHAT_SAMPLES = {
    "us": [
        ("ViperShot", "cyber_ninja", "Ascendant 3", "US", "Any chill Ascendant+ duo down for some Valorant comp? Have mic and comms."),
        ("FrostBite", "arctic_sniper", "Crimson", "CA", "I can flex on NA East if you need a smokes or sentinel player!"),
        ("ViperShot", "cyber_ninja", "Ascendant 3", "US", "Bet, let's run a duo game in 5 mins! Check DMs.")
    ],
    "gb": [
        ("NeonValkyrie", "neon_pilot", "Master", "GB", "Evening lads! Looking for a 3rd for Diamond/Master Apex lobbies."),
        ("ShadowStriker", "tactical_ghost", "Faceit Lvl 9", "DE", "London servers feel super crisp tonight, 18ms ping."),
        ("NeonValkyrie", "neon_pilot", "Master", "GB", "Yeah routing is great today. Drop your tag if you want in!")
    ],
    "ca": [
        ("FrostBite", "arctic_sniper", "Crimson", "CA", "Toronto weather is freezing but the aim is heated today 🔥"),
        ("ViperShot", "cyber_ninja", "Ascendant 3", "US", "NA North servers queue times are instant right now."),
        ("FrostBite", "arctic_sniper", "Crimson", "CA", "Anyone grinding Warzone rebirth? Need 2 with comms.")
    ],
    "de": [
        ("ShadowStriker", "tactical_ghost", "Faceit Lvl 9", "DE", "Moin Leute! CS2 Premier 5-Stack gesucht. 15k-20k Elo."),
        ("NordicGhost", "tactical_ghost", "Faceit Lvl 10", "SE", "Kann mitspielen, bin Lvl 10 und spiele AWP/Support."),
        ("ShadowStriker", "tactical_ghost", "Faceit Lvl 9", "DE", "Perfekt! Habe dir eine Freundschaftsanfrage geschickt.")
    ],
    "fr": [
        ("PixelPhoenix", "neon_pilot", "Grand Champion I", "FR", "Salut la commu ! Dispo pour Rocket League 2v2 ou 3v3 GC."),
        ("NeonValkyrie", "neon_pilot", "Master", "GB", "GGs on that tournament run last weekend!"),
        ("PixelPhoenix", "neon_pilot", "Grand Champion I", "FR", "Merci frérot ! On continue le grind ce soir.")
    ],
    "jp": [
        ("SakuraBlade", "cyber_samurai", "Immortal 1", "JP", "みなさんこんばんは！VCT見ながらValorantコンペ回してます。"),
        ("Kabora_KR", "mech_warrior", "Grandmaster", "KR", "東京サーバーでVALORANT回せますよ！デュオしましょう。"),
        ("SakuraBlade", "cyber_samurai", "Immortal 1", "JP", "ぜひ！VCありで楽しくやりましょうー！")
    ],
    "kr": [
        ("Kabora_KR", "mech_warrior", "Grandmaster", "KR", "롤 솔랭 돌리는 분 계신가요? 다이아~마스터 정글 듀오 구합니다."),
        ("SakuraBlade", "cyber_samurai", "Immortal 1", "JP", "韓国サーバーピン30msで安定してます！"),
        ("Kabora_KR", "mech_warrior", "Grandmaster", "KR", "좋습니다, 디엠 보내주세요!")
    ],
    "br": [
        ("FuriousBR", "bionic_brawler", "Global Elite", "BR", "Fala tropa! Alguém pra fechar lobby de CS2 na GamersClub / Premier?"),
        ("MatadorES", "bionic_brawler", "Diamond 2", "ES", "Boa sorte no grind aí parceiro!"),
        ("FuriousBR", "bionic_brawler", "Global Elite", "BR", "Valeu irmão, bora pra cima sem tiltar!")
    ],
    "au": [
        ("AussieAimer", "cyber_ninja", "Master 4", "AU", "G'day mates! Anyone on Sydney servers for late night Overwatch or Valo?"),
        ("FrostBite", "arctic_sniper", "Crimson", "CA", "Aussie lobbies must be wild right now haha."),
        ("AussieAimer", "cyber_ninja", "Master 4", "AU", "Proper sweaty matches tonight mate, loving it.")
    ],
    "se": [
        ("NordicGhost", "tactical_ghost", "Faceit Lvl 10", "SE", "Tjena! Söker seriösa spelare för Faceit grind ikväll. Stockholm server."),
        ("ShadowStriker", "tactical_ghost", "Faceit Lvl 9", "DE", "Always down to play with Nordic CS players, great aim."),
        ("NordicGhost", "tactical_ghost", "Faceit Lvl 10", "SE", "Tack! Join squad lobby 3, we need 1 more.")
    ],
    "pl": [
        ("HussarPL", "mech_warrior", "Divine 3", "PL", "Siemanko! Ktoś chętny na ranked Dota 2 albo CS2 Katowice server?"),
        ("ShadowStriker", "tactical_ghost", "Faceit Lvl 9", "DE", "Katowice LAN memories are eternal. Good luck in queue!"),
        ("HussarPL", "mech_warrior", "Divine 3", "PL", "Dzięki wielkie! Zapraszam do składu.")
    ],
    "es": [
        ("MatadorES", "bionic_brawler", "Diamond 2", "ES", "Buenas tardes gente! Busco dúo para Valorant diamante/ascendant."),
        ("OrangeFlashNL", "neon_pilot", "Immortal 2", "NL", "Puedo ayudarte con humos si quieres subir rápido!"),
        ("MatadorES", "bionic_brawler", "Diamond 2", "ES", "Hombre muchas gracias, te agrego a amigos ya mismo.")
    ],
    "it": [
        ("GladiatoreIT", "cyber_samurai", "Emerald 1", "IT", "Ciao a tutti! Qualcuno per Rainbow Six Siege stack su server Milano?"),
        ("MatadorES", "bionic_brawler", "Diamond 2", "ES", "Saludos desde España colega!"),
        ("GladiatoreIT", "cyber_samurai", "Emerald 1", "IT", "Grande! Se giochi a R6 o Valo facciamo qualche partita insieme.")
    ],
    "mx": [
        ("AztecaMX", "arctic_sniper", "Diamond 3", "MX", "Qué onda compas! Armando squad para Warzone Rebirth. Con micro por favor!"),
        ("FuriousBR", "bionic_brawler", "Global Elite", "BR", "Boa sorte aí na squad!"),
        ("AztecaMX", "arctic_sniper", "Diamond 3", "MX", "Gracias carnal, tenemos 2 espacios libres si alguien se anima.")
    ],
    "nl": [
        ("OrangeFlashNL", "neon_pilot", "Immortal 2", "NL", "Hallo allemaal! Amsterdam server 4ms ping feels like playing on LAN."),
        ("PixelPhoenix", "neon_pilot", "Grand Champion I", "FR", "EU West servers are the best for real."),
        ("OrangeFlashNL", "neon_pilot", "Immortal 2", "NL", "Absoluut! Open squad for anyone wanting fast tactical executes.")
    ]
}

SAMPLE_SQUADS = [
    {
        "title": "⚡ Ascendant / Immortal Push - Chill Comms, No Tilt",
        "game": "Valorant",
        "mode": "Competitive / Ranked",
        "rank_req": "Diamond 3 - Ascendant 3",
        "mic_req": "Mic Required",
        "region": "NA (East / West)",
        "max_players": 5,
        "discord_voice": "https://discord.gg/respawn-squad-na",
        "leader_user": "vipershot",
        "members": [("vipershot", "IGL / Shotcaller", 1), ("frostbite_ca", "Sniper / Anchor", 1)]
    },
    {
        "title": "🔥 Master Ranked Grind - Aggressive Rotations",
        "game": "Apex Legends",
        "mode": "Competitive / Ranked",
        "rank_req": "Diamond 1 - Master",
        "mic_req": "Mic Required",
        "region": "EU West",
        "max_players": 3,
        "discord_voice": "https://discord.gg/respawn-apex-eu",
        "leader_user": "neonvalkyrie",
        "members": [("neonvalkyrie", "Entry Fragger", 1), ("pixelphoenix", "Support / Healer", 0)]
    },
    {
        "title": "🎯 Faceit Level 8-10 Premier 5-Stack (Frankfurt/Stockholm)",
        "game": "CS2",
        "mode": "Competitive / Ranked",
        "rank_req": "Faceit Lvl 8+",
        "mic_req": "Mic Required",
        "region": "EU Central",
        "max_players": 5,
        "discord_voice": "https://discord.gg/respawn-cs2-eu",
        "leader_user": "shadowstriker",
        "members": [("shadowstriker", "Entry Fragger", 1), ("nordicviking", "Sniper / Anchor", 1), ("hussar_aim", "Flex", 1)]
    },
    {
        "title": "🏆 High Elo Flex Queue / Clash Practice (Seoul Server)",
        "game": "League of Legends",
        "mode": "Tournament / Scrims",
        "rank_req": "Master+",
        "mic_req": "Mic Required",
        "region": "East Asia",
        "max_players": 5,
        "discord_voice": "",
        "leader_user": "kabora",
        "members": [("kabora", "IGL / Shotcaller", 1), ("sakurablade", "Flex", 1)]
    },
    {
        "title": "🍻 Friday Night Chill Rebirth Sweepers - 20+ Bombs",
        "game": "Warzone",
        "mode": "Casual / Chill",
        "rank_req": "Any Rank",
        "mic_req": "Push to Talk",
        "region": "Latin America North",
        "max_players": 4,
        "discord_voice": "https://discord.gg/respawn-wz-latam",
        "leader_user": "azteca_warrior",
        "members": [("azteca_warrior", "Entry Fragger", 1)]
    },
    {
        "title": "🚀 High C3 / GC1 Passing Play & Comms",
        "game": "Rocket League",
        "mode": "Competitive / Ranked",
        "rank_req": "Champion 3 - GC1",
        "mic_req": "Mic Required",
        "region": "EU West",
        "max_players": 3,
        "discord_voice": "",
        "leader_user": "pixelphoenix",
        "members": [("pixelphoenix", "Flex", 1), ("orange_flash", "Support / Healer", 1)]
    }
]

def seed_database():
    with get_db_cursor(commit=True) as cur:
        # Check if users already seeded
        cur.execute("SELECT count(*) as count FROM users")
        if cur.fetchone()["count"] > 0:
            return  # Already seeded
        
        user_ids = {}
        # Seed users
        for u in SAMPLE_USERS:
            pw = hash_password("ProGamer2026!")
            cur.execute("""
                INSERT INTO users (
                    username, email, password_hash, gamer_tag, country,
                    bio, avatar, primary_game, rank, platform,
                    mic_status, discord_tag, karma_score, is_online
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 1)
            """, (
                u["username"], u["email"], pw, u["gamer_tag"], u["country"],
                u["bio"], u["avatar"], u["primary_game"], u["rank"], u["platform"],
                u["mic_status"], u["discord_tag"], u["karma_score"]
            ))
            user_ids[u["username"]] = cur.lastrowid

        # Seed Chat Messages for 15 countries
        for room_id, messages in COUNTRY_CHAT_SAMPLES.items():
            for tag, avatar, rank, country, msg in messages:
                # Find matching user id
                uid = 1
                for uname, uid_val in user_ids.items():
                    if uname.lower() in tag.lower():
                        uid = uid_val
                        break
                cur.execute("""
                    INSERT INTO chat_messages (room_id, user_id, gamer_tag, avatar, rank, country, message)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (room_id, uid, tag, avatar, rank, country, msg))

        # Seed Squads
        for sq in SAMPLE_SQUADS:
            leader_id = user_ids.get(sq["leader_user"], 1)
            cur.execute("""
                INSERT INTO squads (leader_id, title, game, mode, rank_req, mic_req, region, max_players, discord_voice, status)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, 'open')
            """, (leader_id, sq["title"], sq["game"], sq["mode"], sq["rank_req"], sq["mic_req"], sq["region"], sq["max_players"], sq["discord_voice"]))
            squad_id = cur.lastrowid
            
            for mem_uname, role, ready in sq["members"]:
                uid = user_ids.get(mem_uname, 1)
                cur.execute("""
                    INSERT INTO squad_members (squad_id, user_id, role, is_ready)
                    VALUES (?, ?, ?, ?)
                """, (squad_id, uid, role, ready))

        # Seed some mutual friendships
        pairs = [
            ("vipershot", "neonvalkyrie"),
            ("vipershot", "frostbite_ca"),
            ("shadowstriker", "nordicviking"),
            ("kabora", "sakurablade"),
            ("pixelphoenix", "orange_flash")
        ]
        for u1, u2 in pairs:
            id1 = user_ids.get(u1)
            id2 = user_ids.get(u2)
            if id1 and id2:
                cur.execute("INSERT OR IGNORE INTO friends (user_id, friend_id, status) VALUES (?, ?, 'accepted')", (id1, id2))
                cur.execute("INSERT OR IGNORE INTO friends (user_id, friend_id, status) VALUES (?, ?, 'accepted')", (id2, id1))

        # Seed some sample Direct Messages
        dm_samples = [
            ("vipershot", "frostbite_ca", "Yo Frost! Down for some games after dinner?"),
            ("frostbite_ca", "vipershot", "Yessir! Let's lock in around 8 PM EST."),
            ("neonvalkyrie", "vipershot", "Hey Viper, loved your utility callouts in that last scrim."),
            ("vipershot", "neonvalkyrie", "Thanks Valk! Appreciate the hype entry play.")
        ]
        for s_user, r_user, msg in dm_samples:
            s_id = user_ids.get(s_user)
            r_id = user_ids.get(r_user)
            if s_id and r_id:
                cur.execute("""
                    INSERT INTO direct_messages (sender_id, receiver_id, message, is_read)
                    VALUES (?, ?, ?, 1)
                """, (s_id, r_id, msg))

        # Seed sample Karma endorsements
        endorsements = [
            ("frostbite_ca", "vipershot", "Shotcaller"),
            ("neonvalkyrie", "vipershot", "Tilt-Proof"),
            ("vipershot", "frostbite_ca", "Clutch God"),
            ("shadowstriker", "nordicviking", "Good Vibes")
        ]
        for f_user, t_user, cat in endorsements:
            f_id = user_ids.get(f_user)
            t_id = user_ids.get(t_user)
            if f_id and t_id:
                cur.execute("""
                    INSERT INTO karma_endorsements (from_user_id, to_user_id, category)
                    VALUES (?, ?, ?)
                """, (f_id, t_id, cat))
