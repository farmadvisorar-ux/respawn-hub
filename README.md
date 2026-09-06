# 🎯 RESPAWN // SQUADFINDER
### Enterprise-Grade Gamer Matchmaking & Squad Hub

[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy?repo=https://github.com/farmadvisorar-ux/respawn-hub)
[![License: MIT](https://img.shields.io/badge/License-MIT-cyan.svg)](https://opensource.org/licenses/MIT)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.141+-009688.svg?logo=fastapi)](https://fastapi.tiangolo.com)
[![Python 3.14](https://img.shields.io/badge/Python-3.14+-3776AB.svg?logo=python)](https://python.org)
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED.svg?logo=docker)](https://docker.com)

> Built by competitive players for competitive and casual gamers. Zero-lag matchmaking, 15 national hubs, 7 world language rooms, instant squads (Fortnite, Minecraft, Roblox, Call of Duty, Valorant, CS2), private encrypted DMs, friend presence, peer karma endorsements to eradicate toxicity, and an SEO/LLM gaming guides hub.

---

## ⚡ Pro-Gamer Architecture & Features

- **🌐 15 Universal National Flag Chat Rooms**:
  Connect instantly with players in your geographic region and preferred gaming culture. Each room features national flags, live member telemetry, low-latency WebSocket messaging, and regional servers:
  1. 🇺🇸 **United States** (NA East/West)
  2. 🇬🇧 **United Kingdom** (EU West)
  3. 🇨🇦 **Canada** (NA North)
  4. 🇩🇪 **Germany** (EU Central / DACH)
  5. 🇫🇷 **France** (EU West)
  6. 🇯🇵 **Japan** (Asia-Pacific / Tokyo)
  7. 🇰🇷 **South Korea** (East Asia / Seoul)
  8. 🇧🇷 **Brazil** (South America)
  9. 🇦🇺 **Australia** (Oceania / Sydney)
  10. 🇸🇪 **Sweden** (Nordics / Stockholm)
  11. 🇵🇱 **Poland** (EU East / Katowice)
  12. 🇪🇸 **Spain** (EU South / Superliga)
  13. 🇮🇹 **Italy** (EU South / Milan)
  14. 🇲🇽 **Mexico** (LATAM North)
  15. 🇳🇱 **Netherlands** (EU West / Amsterdam)

- **🛡️ LFG Squad Finder (Lobby System)**:
  - Create and discover squad lobbies filtered by **Game** (Valorant, CS2, Apex Legends, League of Legends, Warzone, Rocket League, Overwatch 2, etc.), **Mode** (Competitive / Ranked, Casual / Chill, Tournament / Scrims), and **Region**.
  - Specify mic rules (Mic Required, Push-to-Talk, Listening Only) and role needs (IGL, Entry Fragger, Support, Sniper, Flex).
  - One-click party join with instant squad roster sync.
  - **Ready-Check System**: Squad leader can trigger a live 15-second visual and audio "Ready Check" buzzer for all party members before queueing.
  - One-click Discord voice room linking.

- **💬 Real-Time Direct Messaging (DMs)**:
  - Private 1-on-1 real-time chat with online status, timestamps, and unread notification counters.

- **👥 Friends & Presence Tracker**:
  - Search gamers by GamerTag or username.
  - Pending request notifications, accept/decline flows, and live presence indicators (*Online, In Squad, In Match, Away*).

- **⭐ Anti-Toxic Gamer Karma & Endorsements**:
  - Endorse teammates after matches across 4 core competitive badges:
    - 🧠 **Shotcaller** (+5 Karma): High game IQ, tactical executes, calm round rotations.
    - 🛡️ **Tilt-Proof** (+5 Karma): Positive mental attitude, never gives up when behind.
    - ⚡ **Clutch God** (+5 Karma): High-pressure round closer, laser aim in 1vX scenarios.
    - 🤝 **Good Vibes** (+5 Karma): Friendly, supportive, elevates team morale.

- **🔊 Web Audio API Synthesizer**:
  - Ultra-low latency, zero external asset downloads. High-impact synthesized esports audio for ready checks, notification chimes, and chat pops with a top-bar master mute toggle.

---

## 🚀 Quickstart Guide

### 1. Requirements
- Python 3.10+ (or [uv](https://github.com/astral-sh/uv))
- Git

### 2. Run Locally
```bash
# Clone the repository
git clone https://github.com/your-username/respawn-hub.git
cd respawn-hub

# Create virtual environment and install dependencies
uv venv
uv pip install -r requirements.txt

# Start the application server
python server.py
```
Open [http://127.0.0.1:8000](http://127.0.0.1:8000) in any browser!

---

## 🧪 Automated Verification
Run the automated test suite to verify all 13 core modules:
```bash
python verify_all.py
```

---

## 🌐 Live HTTPS Deployment

### Option A: Instant Live Public HTTPS Tunnel (1-Click)
Run the bundled HTTPS tunnel generator to instantly expose the local server to a public HTTPS URL:
```bash
python tunnel.py
```
This gives you an immediate `https://*.trycloudflare.com` or `https://*.loca.lt` URL with valid SSL certificates.

### Option B: Deploy to Render / Railway / Fly.io (Free Cloud Hosting)
This repository includes production configurations:
- `render.yaml` - 1-click deploy to [Render.com](https://render.com)
- `Dockerfile` - Containerized multi-stage production deployment
- `fly.toml` - Ready for [Fly.io](https://fly.io)

---

## 📄 License
MIT License. Built for the global gaming community.
