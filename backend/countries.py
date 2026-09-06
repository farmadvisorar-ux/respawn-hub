# 15 Regional Country Chat Rooms + World Language Hubs
# Fully localized with native language metadata, localized quick phrases, and server routing

COUNTRIES = [
    {
        "id": "us",
        "code": "US",
        "name": "United States",
        "flag": "🇺🇸",
        "category": "national",
        "region": "NA (East / West)",
        "language": "English (US)",
        "language_native": "English",
        "language_code": "en",
        "hub": "Ashburn / Silicon Valley",
        "popular_games": ["Valorant", "Fortnite", "Call of Duty", "Roblox", "Minecraft"],
        "tagline": "NA Ranked Grind & College Esports",
        "welcome_msg": "Welcome to the United States Hub! Connect with NA East and West players with low ping.",
        "input_placeholder": "Type message in English... (Enter to send)",
        "quick_phrases": [
            {"label": "🎯 Looking for duo", "text": "Looking for +1 duo with mic right now!"},
            {"label": "⚡ Add me for comp", "text": "Anyone grinding comp tonight? Add me!"},
            {"label": "📡 Server ping check", "text": "How is the server ping right now?"},
            {"label": "🔥 Clutch play! GG", "text": "Huge round, well played! GG"}
        ]
    },
    {
        "id": "gb",
        "code": "GB",
        "name": "United Kingdom",
        "flag": "🇬🇧",
        "category": "national",
        "region": "EU West",
        "language": "English (UK)",
        "language_native": "English",
        "language_code": "en",
        "hub": "London",
        "popular_games": ["CS2", "Fortnite", "Call of Duty", "Minecraft", "Rocket League"],
        "tagline": "UK LFG & Competitive Ladders",
        "welcome_msg": "Welcome to the UK Gaming Hub! Connect with UK & Ireland players on London servers.",
        "input_placeholder": "Type message in English... (Enter to send)",
        "quick_phrases": [
            {"label": "🎯 LF Duo w/ mic", "text": "Evening lads! Looking for a duo/trio with mic."},
            {"label": "⚡ Comp grind tonight", "text": "Anyone down for some sweaty comp games tonight?"},
            {"label": "📡 London ping check", "text": "London servers running crisp tonight?"},
            {"label": "🔥 Proper GG", "text": "Proper play mate, love that! GG"}
        ]
    },
    {
        "id": "ca",
        "code": "CA",
        "name": "Canada",
        "flag": "🇨🇦",
        "category": "national",
        "region": "NA North",
        "language": "English & Français",
        "language_native": "English / FR",
        "language_code": "en",
        "hub": "Montreal / Toronto / Vancouver",
        "popular_games": ["Valorant", "Call of Duty", "Minecraft", "Apex Legends", "Fortnite"],
        "tagline": "Chill Vibes & Competitive Scrims",
        "welcome_msg": "Bienvenue au Canada Hub! Great ping to Montreal, Toronto, and Central servers.",
        "input_placeholder": "Type in English or French... (Enter to send)",
        "quick_phrases": [
            {"label": "🎯 Duo LFG", "text": "Looking for duo on NA East/Central with mic!"},
            {"label": "🍁 Scrims tonight", "text": "Anyone queueing scrims or ranked tonight?"},
            {"label": "📡 Ping check", "text": "Central server queue times feeling great today."},
            {"label": "🔥 Great round!", "text": "Awesome clutch, let's keep the streak going!"}
        ]
    },
    {
        "id": "de",
        "code": "DE",
        "name": "Germany",
        "flag": "🇩🇪",
        "category": "national",
        "region": "EU Central",
        "language": "Deutsch (German)",
        "language_native": "Deutsch",
        "language_code": "de",
        "hub": "Frankfurt",
        "popular_games": ["CS2", "Minecraft", "Rainbow Six Siege", "Valorant", "Fortnite"],
        "tagline": "DACH Esports & Taktische Squads",
        "welcome_msg": "Herzlich willkommen im deutschen Gaming-Hub! Verbinde dich mit DACH-Spielern auf Frankfurt-Servern.",
        "input_placeholder": "Nachricht auf Deutsch eingeben... (Enter zum Senden)",
        "quick_phrases": [
            {"label": "🎯 Suche Duo (Mit Mic)", "text": "Suche Duo mit Headset/Mic für Ranked!"},
            {"label": "⚡ Ranked heute Abend", "text": "Jemand Bock auf Premier / Comp heute Abend?"},
            {"label": "📡 Server-Ping Check", "text": "Wie ist euer Ping auf den Frankfurt-Servern gerade?"},
            {"label": "🔥 Stark gespielt! GG", "text": "Stark gespielt Leute! GG"}
        ]
    },
    {
        "id": "fr",
        "code": "FR",
        "name": "France",
        "flag": "🇫🇷",
        "category": "national",
        "region": "EU West",
        "language": "Français (French)",
        "language_native": "Français",
        "language_code": "fr",
        "hub": "Paris",
        "popular_games": ["Valorant", "Rocket League", "League of Legends", "CS2"],
        "tagline": "LFL Énergie & Stacks Compétitifs",
        "welcome_msg": "Bienvenue sur le hub gaming français ! Trouvez vos coéquipiers francophones avec micro.",
        "input_placeholder": "Écrivez votre message en français... (Entrée pour envoyer)",
        "quick_phrases": [
            {"label": "🎯 Cherche duo avec micro", "text": "Salut ! Cherche duo sérieux avec micro pour ranked."},
            {"label": "⚡ Dispo pour comp", "text": "Dispo pour grind ce soir, ajoutez-moi !"},
            {"label": "📡 Check ping Paris", "text": "Comment est votre ping sur les serveurs Paris ?"},
            {"label": "🔥 Bien joué ! GG", "text": "Super clutch bien joué les gars ! GG"}
        ]
    },
    {
        "id": "jp",
        "code": "JP",
        "name": "Japan",
        "flag": "🇯🇵",
        "category": "national",
        "region": "Asia-Pacific",
        "language": "日本語 (Japanese)",
        "language_native": "日本語",
        "language_code": "ja",
        "hub": "Tokyo",
        "popular_games": ["Apex Legends", "Valorant", "Street Fighter 6", "Overwatch 2"],
        "tagline": "東京サーバー Apex & VCT ランクマッチ",
        "welcome_msg": "日本のゲーマーコミュニティへようこそ！東京サーバーでのパーティーやVC固定メンバーを見つけましょう。",
        "input_placeholder": "日本語でメッセージを入力... (Enterで送信)",
        "quick_phrases": [
            {"label": "🎯 デュオ募集 (VCあり)", "text": "デュオ募集してます！VC通話できる方ぜひ！"},
            {"label": "⚡ 今夜ランク回せる人", "text": "今夜コンペ回せる人いませんか？フレンド送りましょう！"},
            {"label": "📡 東京Ping確認", "text": "東京サーバーのPing安定してますか？"},
            {"label": "🔥 ナイスファイト！GG", "text": "ナイスファイト！GGでした！"}
        ]
    },
    {
        "id": "kr",
        "code": "KR",
        "name": "South Korea",
        "flag": "🇰🇷",
        "category": "national",
        "region": "East Asia",
        "language": "한국어 (Korean)",
        "language_native": "한국어",
        "language_code": "ko",
        "hub": "Seoul",
        "popular_games": ["League of Legends", "Overwatch 2", "Valorant", "PUBG"],
        "tagline": "PC방 문화 & 월드 챔피언 래더",
        "welcome_msg": "한국 게이머 허브에 오신 것을 환영합니다! 솔랭 듀오 및 팀원을 찾아보세요.",
        "input_placeholder": "한국어로 메시지를 입력하세요... (Enter 전송)",
        "quick_phrases": [
            {"label": "🎯 듀오 구함 (마이크)", "text": "듀오 구합니다! 마이크 가능하신 분 연락주세요."},
            {"label": "⚡ 오늘 밤 랭크 모집", "text": "오늘 밤 빡겜 랭크 돌리실 분 구해요!"},
            {"label": "📡 서울 핑 확인", "text": "서울 서버 핑 상태 아주 쾌적하네요."},
            {"label": "🔥 나이스 샷! GG", "text": "나이스 플레이! 수고하셨습니다 GG"}
        ]
    },
    {
        "id": "br",
        "code": "BR",
        "name": "Brazil",
        "flag": "🇧🇷",
        "category": "national",
        "region": "South America",
        "language": "Português (Portuguese)",
        "language_native": "Português",
        "language_code": "pt",
        "hub": "São Paulo",
        "popular_games": ["CS2", "Valorant", "League of Legends", "Free Fire"],
        "tagline": "Paixão Gamer & Entrada Agressiva",
        "welcome_msg": "Bem-vindos ao hub gamer brasileiro! Feche lobby de CS2, Valorant e LoL com microfone.",
        "input_placeholder": "Digite em português... (Enter para enviar)",
        "quick_phrases": [
            {"label": "🎯 Procurando duo (Com mic)", "text": "Fala tropa! Alguém com mic pra fechar duo agora?"},
            {"label": "⚡ Bora subir de elo", "text": "Bora comp hoje à noite sem tiltar! Manda convite."},
            {"label": "📡 Como tá o ping SP?", "text": "Ping no servidor de SP tá liso hoje?"},
            {"label": "🔥 Boa jogada! GG", "text": "Boa jogada tropa! Vamooo GG"}
        ]
    },
    {
        "id": "au",
        "code": "AU",
        "name": "Australia",
        "flag": "🇦🇺",
        "category": "national",
        "region": "Oceania",
        "language": "English (Oceania)",
        "language_native": "English",
        "language_code": "en",
        "hub": "Sydney / Melbourne",
        "popular_games": ["Valorant", "CS2", "Apex Legends", "Dota 2"],
        "tagline": "OCE Banter & Late Night Queues",
        "welcome_msg": "G'day! Welcome to the Australia & Oceania Hub. Sydney and Melbourne server queues.",
        "input_placeholder": "Type message in English... (Enter to send)",
        "quick_phrases": [
            {"label": "🎯 LF Duo w/ mic", "text": "G'day mates! Looking for a +1 duo on Sydney servers."},
            {"label": "⚡ Sweaty comp grind", "text": "Anyone grinding comp tonight? Flick an invite."},
            {"label": "📡 Sydney ping check", "text": "Ping is mint tonight, 12ms to Sydney."},
            {"label": "🔥 Absolute legend! GG", "text": "Cracking clutch mate, GG!"}
        ]
    },
    {
        "id": "se",
        "code": "SE",
        "name": "Sweden",
        "flag": "🇸🇪",
        "category": "national",
        "region": "Nordics",
        "language": "Svenska (Swedish)",
        "language_native": "Svenska",
        "language_code": "sv",
        "hub": "Stockholm",
        "popular_games": ["CS2", "Dota 2", "Valorant", "Rocket League"],
        "tagline": "Nordic CS-Arv & Hög Precision",
        "welcome_msg": "Välkommen till den svenska gaming-hubben! Hitta seriösa spelare för Faceit och comp.",
        "input_placeholder": "Skriv ditt meddelande på svenska... (Enter för att skicka)",
        "quick_phrases": [
            {"label": "🎯 Söker duo (Med mic)", "text": "Tjena! Söker seriös duo med mic för ranked."},
            {"label": "⚡ Comp ikväll", "text": "Någon som vill köra Faceit/Comp ikväll? Lägg till mig."},
            {"label": "📡 Stockholm server ping", "text": "Stockholm-servern flyter på riktigt bra ikväll."},
            {"label": "🔥 Snyggt spelat! GG", "text": "Snyggt lirat gänget! GG"}
        ]
    },
    {
        "id": "pl",
        "code": "PL",
        "name": "Poland",
        "flag": "🇵🇱",
        "category": "national",
        "region": "EU East",
        "language": "Polski (Polish)",
        "language_native": "Polski",
        "language_code": "pl",
        "hub": "Warsaw / Katowice",
        "popular_games": ["CS2", "League of Legends", "Valorant", "Dota 2"],
        "tagline": "Duch Katowickiego Spodka & Clutch",
        "welcome_msg": "Witaj w polskim hubie graczy! Szukaj teamu do CS2, LoLa i Valoranta z polskim voice chatem.",
        "input_placeholder": "Wpisz wiadomość po polsku... (Enter aby wysłać)",
        "quick_phrases": [
            {"label": "🎯 Szukam duo z mikro", "text": "Siemanko! Szukam duo z mikrofonem na rankeda."},
            {"label": "⚡ Ktoś na compa dziś?", "text": "Ktoś chętny na wieczorny grind rankingowy? Dodawać!"},
            {"label": "📡 Ping Warszawa/Katowice", "text": "Jak wam dziś działa serwer Warszawa?"},
            {"label": "🔥 Dobra runda! GG", "text": "Ale piękny clutch, dobra robota! GG"}
        ]
    },
    {
        "id": "es",
        "code": "ES",
        "name": "Spain",
        "flag": "🇪🇸",
        "category": "national",
        "region": "EU South",
        "language": "Español (Castellano)",
        "language_native": "Español",
        "language_code": "es",
        "hub": "Madrid / Barcelona",
        "popular_games": ["Valorant", "League of Legends", "EA FC", "Fortnite"],
        "tagline": "Pasión Superliga & Alta Intensidad",
        "welcome_msg": "¡Bienvenidos a la comunidad española! Encuentra tu dúo con micro para subir de rango en Madrid servers.",
        "input_placeholder": "Escribe tu mensaje en español... (Enter para enviar)",
        "quick_phrases": [
            {"label": "🎯 Busco dúo con micro", "text": "¡Buenas! Busco dúo con micro para ranked serio."},
            {"label": "⚡ ¿Quién para comp?", "text": "¿Alguien para subir de rango hoy? Agregadme."},
            {"label": "📡 Ping Madrid", "text": "¿Qué tal os va el ping a los servidores de Madrid?"},
            {"label": "🔥 ¡Buena partida! GG", "text": "¡Vaya ronda gente! GG"}
        ]
    },
    {
        "id": "it",
        "code": "IT",
        "name": "Italy",
        "flag": "🇮🇹",
        "category": "national",
        "region": "EU South",
        "language": "Italiano (Italian)",
        "language_native": "Italiano",
        "language_code": "it",
        "hub": "Milan / Rome",
        "popular_games": ["Valorant", "Rainbow Six Siege", "EA FC", "CS2"],
        "tagline": "Community Italiana & Ranked Serie",
        "welcome_msg": "Benvenuti nell'hub gaming italiano! Trova compagni di squadra con microfono per scalare le ranked.",
        "input_placeholder": "Scrivi il tuo messaggio in italiano... (Invio per inviare)",
        "quick_phrases": [
            {"label": "🎯 Cerco duo con micro", "text": "Ciao a tutti! Cerco duo con microfono per ranked serie."},
            {"label": "⚡ Chi c'è per comp?", "text": "Qualcuno per rankare stasera? Aggiungetemi!"},
            {"label": "📡 Ping Milano", "text": "Com'è il ping sui server di Milano stasera?"},
            {"label": "🔥 Bella giocata! GG", "text": "Grande clutch ragazzi! GG"}
        ]
    },
    {
        "id": "mx",
        "code": "MX",
        "name": "Mexico",
        "flag": "🇲🇽",
        "category": "national",
        "region": "Latin America North",
        "language": "Español (Latino)",
        "language_native": "Español",
        "language_code": "es",
        "hub": "Mexico City / Monterrey",
        "popular_games": ["Valorant", "League of Legends", "Warzone", "Halo"],
        "tagline": "Comunidad LATAM Norte & Squad LFG",
        "welcome_msg": "¡Qué onda compas! Bienvenidos al hub de México y LATAM Norte. Juega con micro y buenas vibras.",
        "input_placeholder": "Escribe en español... (Enter para enviar)",
        "quick_phrases": [
            {"label": "🎯 Busco squad (Con micro)", "text": "¡Qué onda! Busco squad o dúo con micro para ranked."},
            {"label": "⚡ Ranked hoy con todo", "text": "¿Quién para jugar comp hoy? Agreguen sin pena."},
            {"label": "📡 Ping LATAM", "text": "¿Cómo les va el ping hoy en servidores del norte?"},
            {"label": "🔥 ¡Buena jugada! GG", "text": "¡Qué buena ronda carnales! GG"}
        ]
    },
    {
        "id": "nl",
        "code": "NL",
        "name": "Netherlands",
        "flag": "🇳🇱",
        "category": "national",
        "region": "EU West",
        "language": "Nederlands (Dutch)",
        "language_native": "Nederlands",
        "language_code": "nl",
        "hub": "Amsterdam",
        "popular_games": ["Rocket League", "Valorant", "League of Legends", "CS2"],
        "tagline": "Ultra-Low Ping & Tactische Comms",
        "welcome_msg": "Welkom in de Nederlandse gaming-hub! Profiteer van 4ms ping op Amsterdam-servers met een vaste squad.",
        "input_placeholder": "Typ je bericht in het Nederlands... (Enter om te versturen)",
        "quick_phrases": [
            {"label": "🎯 Zoek duo met mic", "text": "Hallo! Zoek een serieuze duo met microfoon voor ranked."},
            {"label": "⚡ Comp vanavond", "text": "Wie heeft er zin om vanavond te grinden? Voeg me toe!"},
            {"label": "📡 Amsterdam 4ms ping", "text": "Amsterdam server ping is weer vlijmscherp vanavond."},
            {"label": "🔥 Lekker gespeeld! GG", "text": "Lekker gespeeld mannen! GG"}
        ]
    }
]

# Additional World Language Hubs & Multilingual Channels
OTHER_LANGUAGE_ROOMS = [
    {
        "id": "global",
        "code": "UN",
        "name": "Global Multilingual",
        "flag": "🌐",
        "category": "other_language",
        "region": "Worldwide",
        "language": "All Languages / Lingua Franca",
        "language_native": "Multilingual",
        "language_code": "all",
        "hub": "Global CDN / Anycast",
        "popular_games": ["Valorant", "CS2", "Fortnite", "Minecraft", "League of Legends"],
        "tagline": "Universal Gaming Lounge - Any Language Welcome",
        "welcome_msg": "Welcome to the RESPAWN Global Multilingual Lounge! Connect with gamers from any country in any language.",
        "input_placeholder": "Type in any language... (Enter to send)",
        "quick_phrases": [
            {"label": "🎯 LFG Any game w/ mic", "text": "Looking for chill teammates for ranked/casual right now!"},
            {"label": "⚡ Add me for games", "text": "Anyone playing comp tonight? Add my gamertag!"},
            {"label": "🌐 Welcome all", "text": "What games is everyone playing tonight?"},
            {"label": "🔥 GG to all!", "text": "Good game everyone, great team spirit!"}
        ]
    },
    {
        "id": "cn",
        "code": "CN",
        "name": "Chinese Gaming Hub",
        "flag": "🇨🇳",
        "category": "other_language",
        "region": "East Asia & Diaspora",
        "language": "中文 (Mandarin / Chinese)",
        "language_native": "中文",
        "language_code": "zh",
        "hub": "Hong Kong / Taipei / Global",
        "popular_games": ["Valorant", "CS2", "Black Myth: Wukong", "League of Legends", "Dota 2"],
        "tagline": "中文玩家联机交流 & 排位开黑组队",
        "welcome_msg": "欢迎来到中文玩家游戏社区！寻找带麦排位队友、开黑连麦、战术交流。",
        "input_placeholder": "中文输入消息... (按Enter发送)",
        "quick_phrases": [
            {"label": "🎯 组队开黑 (带麦)", "text": "有没有打无畏契约或者CS2的？来个带麦的队友！"},
            {"label": "⚡ 今晚排位上分", "text": "今晚有一起排位上分的吗？加个好友一起冲！"},
            {"label": "📡 港服延迟测试", "text": "大家今天连港服和亚服延迟怎么样？"},
            {"label": "🔥 打得漂亮！GG", "text": "残局打得太漂亮了！GG！"}
        ]
    },
    {
        "id": "tr",
        "code": "TR",
        "name": "Turkey (Türkçe)",
        "flag": "🇹🇷",
        "category": "other_language",
        "region": "EU East / Middle East",
        "language": "Türkçe (Turkish)",
        "language_native": "Türkçe",
        "language_code": "tr",
        "hub": "Istanbul / Frankfurt",
        "popular_games": ["Valorant", "CS2", "PUBG", "League of Legends"],
        "tagline": "Türkiye Espor & Rekabetçi Takımlar",
        "welcome_msg": "Türk Oyuncu Topluluğuna hoş geldiniz! İstanbul ve Frankfurt sunucularında mikrofonlu duo/ekip bulun.",
        "input_placeholder": "Türkçe mesajınızı yazın... (Göndermek için Enter)",
        "quick_phrases": [
            {"label": "🎯 Mikrofonlu duo aranır", "text": "Selamlar! Valorant veya CS2 için mikrofonlu duo aranıyor."},
            {"label": "⚡ Akşam rank kasacak var mı?", "text": "Akşam rank kasacak var mı beyler? İstek atın."},
            {"label": "📡 İstanbul ping durumu", "text": "İstanbul sunucusunda ping durumu nasıl şu an?"},
            {"label": "🔥 Helal olsun! GG", "text": "Çok iyi raunttu beyler, helal! GG"}
        ]
    },
    {
        "id": "mena",
        "code": "SA",
        "name": "Arab Gaming Hub",
        "flag": "🇸🇦",
        "category": "other_language",
        "region": "Middle East & North Africa",
        "language": "العربية (Arabic)",
        "language_native": "العربية",
        "language_code": "ar",
        "hub": "Bahrain / Dubai / Riyadh",
        "popular_games": ["Valorant", "Call of Duty", "Fortnite", "Rocket League"],
        "tagline": "مجتمع اللاعبين العرب & بطولات الشرق الأوسط",
        "welcome_msg": "أهلاً بكم في مجتمع اللاعبين العرب! ابحث عن خوي للرانكد في سيرفرات الشرق الأوسط والخليج.",
        "input_placeholder": "اكتب رسالتك بالعربية... (اضغط Enter للإرسال)",
        "quick_phrases": [
            {"label": "🎯 مطلوب خوي بالمايك", "text": "السلام عليكم! مطلوب خوي بالمايك للرانكد الحين."},
            {"label": "⚡ أحد يبي يلعب كود/فالو؟", "text": "أحد يبي رانكد الليلة؟ ضيفوني نلعب سوى."},
            {"label": "📡 فحص بنق البحرين", "text": "كيف البنق معكم على سيرفر البحرين اليوم؟"},
            {"label": "🔥 كفو والله! GG", "text": "كفو يا شباب لعب أسطوري! GG"}
        ]
    },
    {
        "id": "vn",
        "code": "VN",
        "name": "Vietnam (Tiếng Việt)",
        "flag": "🇻🇳",
        "category": "other_language",
        "region": "Southeast Asia",
        "language": "Tiếng Việt (Vietnamese)",
        "language_native": "Tiếng Việt",
        "language_code": "vi",
        "hub": "Hanoi / Ho Chi Minh City",
        "popular_games": ["League of Legends", "Valorant", "CS2", "FC Online"],
        "tagline": "Cộng Đồng Game Thủ Việt Nam & Leo Rank",
        "welcome_msg": "Chào mừng đến với Gaming Hub Việt Nam! Tìm đồng đội leo rank máy chủ Đông Nam Á có mic và không toxic.",
        "input_placeholder": "Nhập tin nhắn bằng tiếng Việt... (Nhấn Enter để gửi)",
        "quick_phrases": [
            {"label": "🎯 Tìm duo có mic", "text": "Chào anh em! Cần tìm duo leo rank nghiêm túc có mic nhé."},
            {"label": "⚡ Tối nay ai leo rank không?", "text": "Tối nay ai rảnh kéo rank không? Kết bạn giao lưu nào!"},
            {"label": "📡 Check ping Singapore", "text": "Ping server Singapore/Hong Kong hôm nay thế nào anh em?"},
            {"label": "🔥 Bắn hay lắm! GG", "text": "Bắn quá hay anh em ơi! GG"}
        ]
    },
    {
        "id": "ph",
        "code": "PH",
        "name": "Philippines (Tagalog)",
        "flag": "🇵🇭",
        "category": "other_language",
        "region": "Southeast Asia",
        "language": "Filipino / Tagalog & English",
        "language_native": "Tagalog",
        "language_code": "fil",
        "hub": "Manila",
        "popular_games": ["Valorant", "Dota 2", "Roblox", "MLBB"],
        "tagline": "Pinoy Gaming Tambayan & Ranked Grinders",
        "welcome_msg": "Kamusta mga ka-gamers! Welcome sa Pinoy Gaming Hub. Hanap ng kalaro sa Valo, Dota 2, or Roblox w/ comms.",
        "input_placeholder": "Type in Tagalog or English... (Enter to send)",
        "quick_phrases": [
            {"label": "🎯 LF Duo/Trio w/ comms", "text": "Kamusta mga lods! LF duo or trio sa Valo/Dota with comms!"},
            {"label": "⚡ G comp grind tonight", "text": "Sino g mag-grind ng rank mamayang gabi? Add niyo ko!"},
            {"label": "📡 Manila ping check", "text": "Kumusta ping niyo sa HK or SG server ngayon?"},
            {"label": "🔥 Gg ganda ng laro!", "text": "Lupet ng clutch lods, GGwp!"}
        ]
    },
    {
        "id": "in",
        "code": "IN",
        "name": "India (Hindi & English)",
        "flag": "🇮🇳",
        "category": "other_language",
        "region": "South Asia",
        "language": "हिन्दी & English",
        "language_native": "हिन्दी",
        "language_code": "hi",
        "hub": "Mumbai / Delhi",
        "popular_games": ["Valorant", "BGMI / PUBG", "CS2", "GTA Online"],
        "tagline": "Desi Esports Grinders & Mumbai Server",
        "welcome_msg": "Welcome to the Indian Gaming Hub! Connect with players on Mumbai servers with clear comms.",
        "input_placeholder": "Type in Hindi or English... (Enter to send)",
        "quick_phrases": [
            {"label": "🎯 Looking for duo w/ mic", "text": "Koi duo chahiye Valorant/CS2 ke liye? Mic on hai Mumbai server!"},
            {"label": "⚡ Comp grind tonight", "text": "Aaj raat rank push karte hain, kis kis ko khelna hai?"},
            {"label": "📡 Mumbai ping check", "text": "Mumbai server ping kaisa aa raha hai sabka?"},
            {"label": "🔥 Kya round tha! GG", "text": "Bhai kya clutch mara! GG"}
        ]
    }
]

ALL_ROOMS = COUNTRIES + OTHER_LANGUAGE_ROOMS
COUNTRY_MAP = {c["id"]: c for c in ALL_ROOMS}
