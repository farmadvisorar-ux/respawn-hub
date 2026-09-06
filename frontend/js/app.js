// RESPAWN // SQUADFINDER - Core Client Application State & Real-Time Engine

const AVATAR_MAP = {
  "cyber_ninja": "🥷",
  "neon_pilot": "🚀",
  "tactical_ghost": "👻",
  "mech_warrior": "🤖",
  "cyber_samurai": "⚔️",
  "bionic_brawler": "🥊",
  "arctic_sniper": "🎯"
};

const COUNTRY_FLAGS = {
  "US": "🇺🇸", "GB": "🇬🇧", "CA": "🇨🇦", "DE": "🇩🇪", "FR": "🇫🇷",
  "JP": "🇯🇵", "KR": "🇰🇷", "BR": "🇧🇷", "AU": "🇦🇺", "SE": "🇸🇪",
  "PL": "🇵🇱", "ES": "🇪🇸", "IT": "🇮🇹", "MX": "🇲🇽", "NL": "🇳🇱"
};

// Global State
const state = {
  token: localStorage.getItem("respawn_token") || null,
  user: null,
  currentTab: "squads",
  countries: [],
  activeCountryId: "us",
  activeConvoPartnerId: null,
  activeSquad: null,
  squadsList: [],
  blogsList: [],
  activeBlogArticle: null,
  selectedBlogCategory: "All",
  selectedBlogGame: "All Games",
  // WebSockets
  chatSocket: null,
  userSocket: null,
  squadSocket: null
};

// --- Initialization ---
document.addEventListener("DOMContentLoaded", async () => {
  updateSoundIcon();
  await checkAuth();
  await loadCountries();
  await loadSquads();
  await fetchTelemetry();
  setInterval(fetchTelemetry, 15000);
});

// --- Sound Controls ---
function toggleSound() {
  const isMuted = window.audioManager.toggleMute();
  updateSoundIcon();
  if (!isMuted) {
    window.audioManager.playNotification();
  }
}

function updateSoundIcon() {
  const icon = document.getElementById("audio-icon");
  if (icon) {
    if (window.audioManager.muted) {
      icon.className = "fa-solid fa-volume-xmark";
      icon.style.color = "var(--neon-coral)";
    } else {
      icon.className = "fa-solid fa-volume-high";
      icon.style.color = "var(--neon-cyan)";
    }
  }
}

// --- Navigation Tabs ---
function switchTab(tabId) {
  state.currentTab = tabId;
  document.querySelectorAll(".tab-panel").forEach(p => p.classList.remove("active"));
  document.querySelectorAll(".nav-link").forEach(l => l.classList.remove("active"));

  const targetPanel = document.getElementById(`tab-${tabId}`);
  const targetNav = document.getElementById(`nav-${tabId}`);
  if (targetPanel) targetPanel.classList.add("active");
  if (targetNav) targetNav.classList.add("active");

  window.audioManager.playClick();

  if (tabId === "chat") {
    selectCountryRoom(state.activeCountryId);
  } else if (tabId === "squads") {
    loadSquads();
  } else if (tabId === "dms") {
    loadDMConversations();
  } else if (tabId === "friends") {
    loadFriends();
  } else if (tabId === "karma") {
    loadKarmaLeaderboard();
  } else if (tabId === "profile") {
    loadProfileSettings();
  } else if (tabId === "blogs") {
    loadBlogArticles();
  }
}

// --- Platform Telemetry ---
async function fetchTelemetry() {
  try {
    const res = await fetch("/api/stats");
    if (res.ok) {
      const data = await res.json();
      document.getElementById("stat-online-gamers").innerText = data.online_gamers;
      document.getElementById("stat-active-squads").innerText = data.active_squads;
    }
  } catch (err) {
    console.warn("Telemetry ping:", err);
  }
}

// --- Authentication ---
async function checkAuth() {
  if (!state.token) {
    renderAuthNav(null);
    return;
  }
  try {
    const res = await fetch("/api/auth/me", {
      headers: { "Authorization": `Bearer ${state.token}` }
    });
    if (res.ok) {
      state.user = await res.json();
      renderAuthNav(state.user);
      connectUserSocket();
    } else {
      state.token = null;
      localStorage.removeItem("respawn_token");
      renderAuthNav(null);
    }
  } catch (err) {
    renderAuthNav(null);
  }
}

function renderAuthNav(user) {
  const container = document.getElementById("auth-nav-container");
  if (!container) return;

  if (user) {
    const flag = COUNTRY_FLAGS[user.country] || "🌐";
    const avatarEmoji = AVATAR_MAP[user.avatar] || "🥷";
    container.innerHTML = `
      <div style="display: flex; align-items: center; gap: 10px; background: var(--bg-surface); border: 1px solid var(--border-subtle); padding: 4px 12px; border-radius: 20px; cursor: pointer;" onclick="switchTab('profile')">
        <div style="font-size: 18px;">${avatarEmoji}</div>
        <div style="text-align: left;">
          <div style="font-size: 13px; font-weight: 700; color: var(--neon-cyan); display: flex; align-items: center; gap: 4px;">
            <span>${user.gamer_tag}</span> <span>${flag}</span>
          </div>
          <div style="font-size: 10px; color: var(--neon-green); font-weight: 600;">
            ⭐ ${user.karma_score} Karma
          </div>
        </div>
        <button onclick="event.stopPropagation(); logout()" style="background: none; border: none; color: var(--text-dim); margin-left: 6px; cursor: pointer;" title="Logout">
          <i class="fa-solid fa-right-from-bracket"></i>
        </button>
      </div>
    `;
  } else {
    container.innerHTML = `
      <button class="btn-icon" style="width: auto; padding: 0 16px; font-weight: 700; font-size: 13px; color: var(--neon-cyan);" onclick="openAuthModal('login')">
        <i class="fa-solid fa-right-to-bracket" style="margin-right: 6px;"></i> SIGN IN
      </button>
    `;
  }
}

function openAuthModal(mode = 'login') {
  toggleAuthTab(mode);
  document.getElementById("modal-auth").classList.add("open");
}

function toggleAuthTab(mode) {
  const loginPane = document.getElementById("form-login-pane");
  const regPane = document.getElementById("form-register-pane");
  const tabLogin = document.getElementById("tab-auth-login");
  const tabReg = document.getElementById("tab-auth-register");
  const title = document.getElementById("auth-modal-title");

  if (mode === 'login') {
    loginPane.style.display = "block";
    regPane.style.display = "none";
    tabLogin.style.background = "var(--neon-cyan)";
    tabLogin.style.color = "#07090e";
    tabReg.style.background = "transparent";
    tabReg.style.color = "var(--text-muted)";
    title.innerText = "PLAYER LOGIN";
  } else {
    loginPane.style.display = "none";
    regPane.style.display = "block";
    tabReg.style.background = "var(--neon-cyan)";
    tabReg.style.color = "#07090e";
    tabLogin.style.background = "transparent";
    tabLogin.style.color = "var(--text-muted)";
    title.innerText = "CREATE PRO ACCOUNT";
  }
}

async function submitLogin() {
  const identifier = document.getElementById("login-username").value.trim();
  const password = document.getElementById("login-password").value;
  if (!identifier || !password) {
    alert("Please enter both username and password");
    return;
  }

  try {
    const res = await fetch("/api/auth/login", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ username_or_email: identifier, password })
    });
    const data = await res.json();
    if (res.ok) {
      state.token = data.token;
      state.user = data.user;
      localStorage.setItem("respawn_token", data.token);
      closeModal("modal-auth");
      renderAuthNav(state.user);
      connectUserSocket();
      window.audioManager.playChord();
    } else {
      alert(data.detail || "Login failed");
    }
  } catch (err) {
    alert("Network error logging in");
  }
}

async function quickDemoLogin(username) {
  document.getElementById("login-username").value = username;
  document.getElementById("login-password").value = "ProGamer2026!";
  await submitLogin();
}

async function submitRegister() {
  const gamer_tag = document.getElementById("reg-gamertag").value.trim();
  const username = document.getElementById("reg-username").value.trim();
  const email = document.getElementById("reg-email").value.trim();
  const password = document.getElementById("reg-password").value;
  const country = document.getElementById("reg-country").value;
  const primary_game = document.getElementById("reg-game").value;
  const platform = document.getElementById("reg-platform").value;

  if (!gamer_tag || !username || !email || !password) {
    alert("Please fill in all required fields");
    return;
  }

  try {
    const res = await fetch("/api/auth/register", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        gamer_tag, username, email, password, country, primary_game, platform, rank: "Diamond", avatar: "cyber_ninja"
      })
    });
    const data = await res.json();
    if (res.ok) {
      state.token = data.token;
      state.user = data.user;
      localStorage.setItem("respawn_token", data.token);
      closeModal("modal-auth");
      renderAuthNav(state.user);
      connectUserSocket();
      window.audioManager.playChord();
    } else {
      alert(data.detail || "Registration failed");
    }
  } catch (err) {
    alert("Network error registering");
  }
}

async function logout() {
  if (state.token) {
    try {
      await fetch("/api/auth/logout", {
        method: "POST",
        headers: { "Authorization": `Bearer ${state.token}` }
      });
    } catch (e) {}
  }
  state.token = null;
  state.user = null;
  localStorage.removeItem("respawn_token");
  if (state.userSocket) {
    state.userSocket.close();
  }
  renderAuthNav(null);
  window.audioManager.playClick();
}

// --- WebSocket User Channel (Direct Messages, Friend Requests, Squad Pings) ---
function connectUserSocket() {
  if (!state.user) return;
  if (state.userSocket) {
    state.userSocket.close();
  }

  const protocol = window.location.protocol === "https:" ? "wss:" : "ws:";
  const wsUrl = `${protocol}//${window.location.host}/ws/user/${state.user.id}`;
  state.userSocket = new WebSocket(wsUrl);

  state.userSocket.onmessage = (event) => {
    try {
      const payload = JSON.parse(event.data);
      if (payload.type === "new_direct_message") {
        window.audioManager.playNotification();
        handleIncomingDM(payload.message);
      } else if (payload.type === "incoming_friend_request") {
        window.audioManager.playNotification();
        showNotification(`${payload.sender.gamer_tag} sent you a friend request!`);
        loadFriends();
      } else if (payload.type === "friend_request_accepted") {
        window.audioManager.playChord();
        showNotification(`${payload.friend.gamer_tag} accepted your friend request!`);
        loadFriends();
      } else if (payload.type === "endorsement_received") {
        window.audioManager.playChord();
        showNotification(`⭐ ${payload.by} endorsed you for '${payload.category}' (+5 Karma)!`);
        if (state.user) {
          state.user.karma_score = payload.new_karma;
          renderAuthNav(state.user);
        }
      }
    } catch (err) {
      console.warn("User socket message parse error:", err);
    }
  };

  // Heartbeat
  setInterval(() => {
    if (state.userSocket && state.userSocket.readyState === WebSocket.OPEN) {
      state.userSocket.send(JSON.stringify({ type: "ping" }));
    }
  }, 25000);
}

// --- 15 National Flag Chat Hub ---
async function loadCountries() {
  try {
    const res = await fetch("/api/countries");
    if (res.ok) {
      state.countries = await res.json();
      renderCountryChips();
    }
  } catch (err) {
    console.error("Failed to load countries:", err);
  }
}

function renderCountryChips() {
  const container = document.getElementById("countries-chips-container");
  if (!container) return;

  container.innerHTML = state.countries.map(c => `
    <div class="country-chip ${c.id === state.activeCountryId ? 'active' : ''}" onclick="selectCountryRoom('${c.id}')" id="chip-${c.id}">
      <span class="chip-flag">${c.flag}</span>
      <span class="chip-name">${c.name}</span>
      <span class="chip-online">${c.online_count} <i class="fa-solid fa-signal fa-2xs"></i></span>
    </div>
  `).join("");
}

async function selectCountryRoom(roomId) {
  state.activeCountryId = roomId;
  renderCountryChips();

  const country = state.countries.find(c => c.id === roomId) || {
    name: "Regional Hub", flag: "🌐", tagline: "Universal Gaming Comms", online_count: 10
  };

  document.getElementById("active-chat-flag").innerText = country.flag;
  document.getElementById("active-chat-name").innerText = `${country.name} Hub`;
  document.getElementById("active-chat-online").innerHTML = `<i class="fa-solid fa-circle fa-2xs"></i> ${country.online_count} Gamers Active`;
  document.getElementById("active-chat-tagline").innerText = country.tagline;

  // Load chat messages
  await refreshActiveRoomChat();

  // Connect WebSocket for room
  connectRoomWebSocket(roomId);
}

async function refreshActiveRoomChat() {
  const stream = document.getElementById("chat-messages-stream");
  try {
    const res = await fetch(`/api/chat/${state.activeCountryId}`);
    if (res.ok) {
      const data = await res.json();
      stream.innerHTML = data.messages.map(m => renderChatMessage(m)).join("");
      stream.scrollTop = stream.scrollHeight;
    }
  } catch (err) {
    console.error("Failed to load room messages:", err);
  }
}

function renderChatMessage(m) {
  const isOwn = state.user && state.user.id === m.user_id;
  const avatarEmoji = AVATAR_MAP[m.avatar] || "🥷";
  const flag = COUNTRY_FLAGS[m.country] || "🌐";
  const time = m.timestamp ? new Date(m.timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }) : "Just now";

  return `
    <div class="chat-msg">
      <div class="chat-avatar" onclick="openGamerCard(${m.user_id})" title="View Gamer Profile">
        ${avatarEmoji}
      </div>
      <div class="chat-bubble ${isOwn ? 'own' : ''}">
        <div class="chat-meta">
          <span class="chat-tag" onclick="openGamerCard(${m.user_id})">${m.gamer_tag}</span>
          <span>${flag}</span>
          <span class="rank-badge rank-diamond">${m.rank}</span>
          <span style="font-size: 11px; color: var(--neon-green); font-weight: 700;">⭐ ${m.karma_score || 15}</span>
          <span class="chat-time">${time}</span>
        </div>
        <div class="chat-body">${escapeHTML(m.message)}</div>
      </div>
    </div>
  `;
}

function connectRoomWebSocket(roomId) {
  if (state.chatSocket) {
    state.chatSocket.close();
  }

  const protocol = window.location.protocol === "https:" ? "wss:" : "ws:";
  const wsUrl = `${protocol}//${window.location.host}/ws/chat/${roomId}`;
  state.chatSocket = new WebSocket(wsUrl);

  state.chatSocket.onmessage = (event) => {
    try {
      const payload = JSON.parse(event.data);
      if (payload.type === "new_chat_message" && payload.room_id === state.activeCountryId) {
        const stream = document.getElementById("chat-messages-stream");
        stream.insertAdjacentHTML("beforeend", renderChatMessage(payload.message));
        stream.scrollTop = stream.scrollHeight;
        window.audioManager.playPop();
      }
    } catch (err) {
      console.warn("Chat WS message parse:", err);
    }
  };
}

async function sendRoomMessage() {
  if (!state.user) {
    openAuthModal('login');
    return;
  }

  const input = document.getElementById("chat-msg-input");
  const text = input.value.trim();
  if (!text) return;

  input.value = "";
  try {
    const res = await fetch(`/api/chat/${state.activeCountryId}`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "Authorization": `Bearer ${state.token}`
      },
      body: JSON.stringify({ message: text })
    });
    if (!res.ok) {
      const err = await res.json();
      alert(err.detail || "Failed to post message");
    }
  } catch (err) {
    console.error("Failed to send message:", err);
  }
}

function insertQuickPhrase(phrase) {
  const input = document.getElementById("chat-msg-input");
  input.value = phrase;
  input.focus();
}

// --- Squad Finder & LFG Lobbies ---
async function loadSquads() {
  const game = document.getElementById("filter-game")?.value || "All Games";
  const mode = document.getElementById("filter-mode")?.value || "All Modes";
  const region = document.getElementById("filter-region")?.value || "All Regions";

  try {
    const params = new URLSearchParams({ game, mode, region });
    const res = await fetch(`/api/squads?${params.toString()}`);
    if (res.ok) {
      state.squadsList = await res.json();
      renderSquadsGrid(state.squadsList);
    }
  } catch (err) {
    console.error("Failed to load squads:", err);
  }
}

function filterSquadsLocally() {
  const q = document.getElementById("search-squads").value.toLowerCase();
  const filtered = state.squadsList.filter(s => 
    s.title.toLowerCase().includes(q) ||
    s.game.toLowerCase().includes(q) ||
    s.leader_tag.toLowerCase().includes(q) ||
    s.rank_req.toLowerCase().includes(q)
  );
  renderSquadsGrid(filtered);
}

function renderSquadsGrid(squads) {
  const container = document.getElementById("squad-grid-container");
  if (!container) return;

  if (squads.length === 0) {
    container.innerHTML = `
      <div style="grid-column: 1/-1; text-align: center; padding: 60px 20px; color: var(--text-dim);">
        <i class="fa-solid fa-gamepad fa-3x" style="margin-bottom: 16px; opacity: 0.4;"></i>
        <h3 style="font-size: 18px; color: var(--text-muted); margin-bottom: 8px;">No Squad Lobbies Found</h3>
        <p style="font-size: 13px; margin-bottom: 16px;">Be the leader and create the first squad with your requirements!</p>
        <button class="btn-squad-create" onclick="openCreateSquadModal()" style="margin: 0 auto;">
          <i class="fa-solid fa-plus"></i> CREATE SQUAD
        </button>
      </div>
    `;
    return;
  }

  container.innerHTML = squads.map(s => {
    const isMember = state.user && s.members.some(m => m.user_id === state.user.id);
    const slotsLeft = s.max_players - s.current_players;
    const leaderAvatar = AVATAR_MAP[s.leader_avatar] || "🥷";

    return `
      <div class="squad-card">
        <div class="squad-top">
          <span class="game-badge">${s.game}</span>
          <span class="squad-slots">${s.current_players}/${s.max_players} PLAYERS</span>
        </div>

        <div class="squad-title">${escapeHTML(s.title)}</div>

        <div class="squad-meta-tags">
          <span class="meta-tag"><i class="fa-solid fa-trophy" style="color: var(--neon-gold);"></i> ${s.mode}</span>
          <span class="meta-tag"><i class="fa-solid fa-medal" style="color: var(--neon-cyan);"></i> ${s.rank_req}</span>
          <span class="meta-tag"><i class="fa-solid fa-microphone" style="color: var(--neon-green);"></i> ${s.mic_req}</span>
          <span class="meta-tag"><i class="fa-solid fa-earth-americas"></i> ${s.region}</span>
        </div>

        <div class="squad-roster">
          ${s.members.map(m => `
            <div class="roster-avatar ${m.is_ready ? 'ready' : ''}" title="${m.gamer_tag} (${m.role}) - ${m.is_ready ? 'READY' : 'Waiting'}">
              ${AVATAR_MAP[m.avatar] || '🥷'}
            </div>
          `).join("")}
          ${Array(Math.max(0, slotsLeft)).fill('<div class="roster-avatar" style="border-style: dashed; opacity: 0.4;"><i class="fa-solid fa-plus fa-2xs"></i></div>').join("")}
        </div>

        <div class="squad-footer">
          <div class="leader-info" onclick="openGamerCard(${s.leader_id})" style="cursor: pointer;">
            <span>${leaderAvatar}</span>
            <span style="font-weight: 700; color: var(--text-main);">${s.leader_tag}</span>
            <span style="color: var(--neon-green); font-size: 11px;">⭐ ${s.leader_karma}</span>
          </div>

          ${isMember ? `
            <button class="btn-join" style="background: var(--neon-cyan); color: #07090e;" onclick="viewSquadDetails(${s.id})">
              OPEN LOBBY
            </button>
          ` : `
            <button class="btn-join" onclick="joinSquadDirect(${s.id})">
              JOIN SQUAD
            </button>
          `}
        </div>
      </div>
    `;
  }).join("");
}

// --- Squad Actions & Modals ---
function openCreateSquadModal() {
  if (!state.user) {
    openAuthModal('login');
    return;
  }
  document.getElementById("modal-create-squad").classList.add("open");
}

async function submitCreateSquad() {
  const title = document.getElementById("squad-title").value.trim();
  const game = document.getElementById("squad-game").value;
  const mode = document.getElementById("squad-mode").value;
  const rank_req = document.getElementById("squad-rank-req").value.trim() || "Any Rank";
  const mic_req = document.getElementById("squad-mic-req").value;
  const region = document.getElementById("squad-region").value;
  const max_players = parseInt(document.getElementById("squad-max-players").value);
  const discord_voice = document.getElementById("squad-discord").value.trim();
  const role = document.getElementById("squad-leader-role").value;

  if (!title) {
    alert("Please provide a title for your squad lobby");
    return;
  }

  try {
    const res = await fetch("/api/squads", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "Authorization": `Bearer ${state.token}`
      },
      body: JSON.stringify({
        title, game, mode, rank_req, mic_req, region, max_players, discord_voice, role
      })
    });
    if (res.ok) {
      const squad = await res.json();
      closeModal("modal-create-squad");
      window.audioManager.playChord();
      await loadSquads();
      await viewSquadDetails(squad.id);
    } else {
      const err = await res.json();
      alert(err.detail || "Failed to create squad");
    }
  } catch (err) {
    alert("Network error creating squad");
  }
}

async function joinSquadDirect(squadId) {
  if (!state.user) {
    openAuthModal('login');
    return;
  }

  try {
    const res = await fetch(`/api/squads/${squadId}/join`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "Authorization": `Bearer ${state.token}`
      },
      body: JSON.stringify({ role: "Flex" })
    });
    if (res.ok) {
      const squad = await res.json();
      window.audioManager.playChord();
      await loadSquads();
      await viewSquadDetails(squadId);
    } else {
      const err = await res.json();
      alert(err.detail || "Unable to join squad");
    }
  } catch (err) {
    alert("Network error joining squad");
  }
}

async function viewSquadDetails(squadId) {
  try {
    const res = await fetch(`/api/squads/${squadId}`);
    if (res.ok) {
      state.activeSquad = await res.json();
      renderActiveSquadModal();
      connectSquadWebSocket(squadId);
      document.getElementById("modal-active-squad").classList.add("open");
      updateSquadDock();
    }
  } catch (err) {
    console.error("Failed to load squad details:", err);
  }
}

function renderActiveSquadModal() {
  const sq = state.activeSquad;
  if (!sq) return;

  document.getElementById("active-squad-title").innerText = sq.title;
  document.getElementById("active-squad-count").innerText = `${sq.current_players}/${sq.max_players}`;

  const isLeader = state.user && sq.leader_id === state.user.id;
  document.getElementById("btn-leader-ready-check").style.display = isLeader ? "block" : "none";

  // Badges
  document.getElementById("active-squad-badges").innerHTML = `
    <span class="game-badge">${sq.game}</span>
    <span class="meta-tag"><i class="fa-solid fa-trophy"></i> ${sq.mode}</span>
    <span class="meta-tag"><i class="fa-solid fa-medal"></i> ${sq.rank_req}</span>
    <span class="meta-tag"><i class="fa-solid fa-microphone"></i> ${sq.mic_req}</span>
    <span class="meta-tag"><i class="fa-solid fa-earth-americas"></i> ${sq.region}</span>
  `;

  // Members list
  document.getElementById("active-squad-members").innerHTML = sq.members.map(m => {
    const isLeaderMember = m.user_id === sq.leader_id;
    return `
      <div style="display: flex; align-items: center; justify-content: space-between; background: var(--bg-core); padding: 10px 14px; border-radius: 8px; border: 1px solid var(--border-subtle);">
        <div style="display: flex; align-items: center; gap: 10px;">
          <div style="font-size: 20px;">${AVATAR_MAP[m.avatar] || '🥷'}</div>
          <div>
            <div style="font-size: 13px; font-weight: 700; display: flex; align-items: center; gap: 6px;">
              <span>${m.gamer_tag}</span>
              ${isLeaderMember ? '<span style="font-size: 10px; background: rgba(255,209,102,0.2); color: var(--neon-gold); padding: 1px 6px; border-radius: 4px;">LEADER</span>' : ''}
            </div>
            <div style="font-size: 11px; color: var(--text-muted); display: flex; gap: 8px; margin-top: 2px;">
              <span>${m.role}</span> &bull;
              <span>${m.rank}</span> &bull;
              <span>${m.platform}</span> &bull;
              <span style="color: var(--neon-green);">⭐ ${m.karma_score} Karma</span>
            </div>
          </div>
        </div>

        <div>
          ${m.is_ready ? `
            <span style="background: rgba(0, 255, 135, 0.15); color: var(--neon-green); font-size: 11px; font-weight: 800; padding: 4px 10px; border-radius: 6px; border: 1px solid var(--neon-green);">
              <i class="fa-solid fa-check"></i> READY
            </span>
          ` : `
            <span style="background: rgba(255, 255, 255, 0.05); color: var(--text-dim); font-size: 11px; font-weight: 700; padding: 4px 10px; border-radius: 6px;">
              NOT READY
            </span>
          `}
        </div>
      </div>
    `;
  }).join("");

  // Discord Voice
  const voiceBox = document.getElementById("active-squad-voice-box");
  const voiceLink = document.getElementById("active-squad-voice-link");
  if (sq.discord_voice) {
    voiceBox.style.display = "flex";
    voiceLink.href = sq.discord_voice;
  } else {
    voiceBox.style.display = "none";
  }
}

function updateSquadDock() {
  const dock = document.getElementById("active-squad-dock");
  const title = document.getElementById("dock-squad-title");
  if (state.activeSquad) {
    dock.style.display = "block";
    title.innerText = state.activeSquad.title;
  } else {
    dock.style.display = "none";
  }
}

function openActiveSquadModal() {
  if (state.activeSquad) {
    document.getElementById("modal-active-squad").classList.add("open");
  }
}

function connectSquadWebSocket(squadId) {
  if (state.squadSocket) {
    state.squadSocket.close();
  }

  const protocol = window.location.protocol === "https:" ? "wss:" : "ws:";
  const wsUrl = `${protocol}//${window.location.host}/ws/squad/${squadId}`;
  state.squadSocket = new WebSocket(wsUrl);

  state.squadSocket.onmessage = (event) => {
    try {
      const payload = JSON.parse(event.data);
      if (payload.type === "member_joined" || payload.type === "member_left" || payload.type === "ready_toggled") {
        state.activeSquad = payload.squad;
        renderActiveSquadModal();
        loadSquads();
      } else if (payload.type === "ready_check_started") {
        window.audioManager.playReadyCheck();
        document.getElementById("ready-check-banner").style.display = "block";
        document.getElementById("ready-check-sender").innerText = `${payload.initiated_by} triggered a Ready Check! Are you locked in?`;
      } else if (payload.type === "squad_disbanded") {
        state.activeSquad = null;
        updateSquadDock();
        closeModal("modal-active-squad");
        loadSquads();
        showNotification("The squad lobby was disbanded by the leader.");
      }
    } catch (err) {
      console.warn("Squad WS message error:", err);
    }
  };
}

async function toggleMyReadyState() {
  if (!state.activeSquad || !state.user) return;
  try {
    const res = await fetch(`/api/squads/${state.activeSquad.id}/ready`, {
      method: "POST",
      headers: { "Authorization": `Bearer ${state.token}` }
    });
    if (res.ok) {
      window.audioManager.playClick();
    }
  } catch (err) {
    console.error("Failed to toggle ready:", err);
  }
}

async function startLeaderReadyCheck() {
  if (!state.activeSquad || !state.user) return;
  try {
    await fetch(`/api/squads/${state.activeSquad.id}/ready-check`, {
      method: "POST",
      headers: { "Authorization": `Bearer ${state.token}` }
    });
  } catch (err) {
    console.error("Failed to start ready check:", err);
  }
}

async function confirmReady() {
  document.getElementById("ready-check-banner").style.display = "none";
  await toggleMyReadyState();
}

async function leaveActiveSquad() {
  if (!state.activeSquad || !state.user) return;
  try {
    await fetch(`/api/squads/${state.activeSquad.id}/leave`, {
      method: "POST",
      headers: { "Authorization": `Bearer ${state.token}` }
    });
    state.activeSquad = null;
    updateSquadDock();
    closeModal("modal-active-squad");
    await loadSquads();
    window.audioManager.playClick();
  } catch (err) {
    console.error("Failed to leave squad:", err);
  }
}

// --- Direct Messaging (DMs) ---
async function loadDMConversations() {
  if (!state.user) {
    openAuthModal('login');
    return;
  }

  try {
    const res = await fetch("/api/dms/conversations", {
      headers: { "Authorization": `Bearer ${state.token}` }
    });
    if (res.ok) {
      const convos = await res.json();
      renderDMConversationsList(convos);
    }
  } catch (err) {
    console.error("Failed to load DMs:", err);
  }
}

function renderDMConversationsList(convos) {
  const container = document.getElementById("dm-convos-list");
  if (!container) return;

  if (convos.length === 0) {
    container.innerHTML = `
      <div style="padding: 24px; text-align: center; color: var(--text-dim); font-size: 12px;">
        No active chats yet. Open a gamer's profile to start a private DM!
      </div>
    `;
    return;
  }

  container.innerHTML = convos.map(c => `
    <div onclick="openDMWithUser(${c.partner.id})" style="padding: 12px 14px; border-bottom: 1px solid var(--border-subtle); display: flex; align-items: center; gap: 10px; cursor: pointer; background: ${state.activeConvoPartnerId === c.partner.id ? 'var(--bg-elevated)' : 'transparent'};">
      <div style="font-size: 22px;">${AVATAR_MAP[c.partner.avatar] || '🥷'}</div>
      <div style="flex: 1; overflow: hidden;">
        <div style="display: flex; justify-content: space-between; align-items: center;">
          <span style="font-size: 13px; font-weight: 700; color: var(--text-main);">${c.partner.gamer_tag}</span>
          ${c.unread_count > 0 ? `<span class="nav-badge">${c.unread_count}</span>` : ''}
        </div>
        <div style="font-size: 11px; color: var(--text-dim); white-space: nowrap; overflow: hidden; text-overflow: ellipsis; margin-top: 2px;">
          ${c.last_message ? escapeHTML(c.last_message.message) : 'Start conversation...'}
        </div>
      </div>
    </div>
  `).join("");
}

async function openDMWithUser(partnerId) {
  state.activeConvoPartnerId = partnerId;
  switchTab("dms");

  try {
    const res = await fetch(`/api/dms/${partnerId}`, {
      headers: { "Authorization": `Bearer ${state.token}` }
    });
    if (res.ok) {
      const data = await res.json();
      const partner = data.partner;
      const headerInfo = document.getElementById("dm-partner-info");
      headerInfo.innerHTML = `
        <div style="font-size: 24px;">${AVATAR_MAP[partner.avatar] || '🥷'}</div>
        <div>
          <div style="font-size: 15px; font-weight: 800; color: var(--text-main);">${partner.gamer_tag}</div>
          <div style="font-size: 11px; color: var(--neon-cyan);">${partner.primary_game} &bull; ${partner.rank} &bull; ⭐ ${partner.karma_score} Karma</div>
        </div>
      `;

      const stream = document.getElementById("dm-messages-stream");
      stream.innerHTML = data.messages.map(m => {
        const isOwn = m.sender_id === state.user.id;
        const time = new Date(m.timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
        return `
          <div class="chat-msg" style="${isOwn ? 'justify-content: flex-end;' : ''}">
            <div class="chat-bubble ${isOwn ? 'own' : ''}">
              <div style="font-size: 11px; color: var(--text-dim); margin-bottom: 2px;">
                ${isOwn ? 'You' : partner.gamer_tag} &bull; ${time}
              </div>
              <div class="chat-body">${escapeHTML(m.message)}</div>
            </div>
          </div>
        `;
      }).join("");

      stream.scrollTop = stream.scrollHeight;
    }
  } catch (err) {
    console.error("Failed to open DM:", err);
  }
}

async function sendDM() {
  if (!state.user || !state.activeConvoPartnerId) return;

  const input = document.getElementById("dm-input-box");
  const text = input.value.trim();
  if (!text) return;

  input.value = "";
  try {
    const res = await fetch(`/api/dms/${state.activeConvoPartnerId}`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "Authorization": `Bearer ${state.token}`
      },
      body: JSON.stringify({ message: text })
    });
    if (res.ok) {
      const msg = await res.json();
      const stream = document.getElementById("dm-messages-stream");
      const time = new Date(msg.timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
      stream.insertAdjacentHTML("beforeend", `
        <div class="chat-msg" style="justify-content: flex-end;">
          <div class="chat-bubble own">
            <div style="font-size: 11px; color: var(--text-dim); margin-bottom: 2px;">
              You &bull; ${time}
            </div>
            <div class="chat-body">${escapeHTML(msg.message)}</div>
          </div>
        </div>
      `);
      stream.scrollTop = stream.scrollHeight;
      window.audioManager.playPop();
    }
  } catch (err) {
    console.error("Failed to send DM:", err);
  }
}

function handleIncomingDM(msg) {
  if (state.activeConvoPartnerId === msg.sender_id && state.currentTab === "dms") {
    const stream = document.getElementById("dm-messages-stream");
    const time = new Date(msg.timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    stream.insertAdjacentHTML("beforeend", `
      <div class="chat-msg">
        <div class="chat-bubble">
          <div style="font-size: 11px; color: var(--text-dim); margin-bottom: 2px;">
            ${msg.sender_tag} &bull; ${time}
          </div>
          <div class="chat-body">${escapeHTML(msg.message)}</div>
        </div>
      </div>
    `);
    stream.scrollTop = stream.scrollHeight;
  } else {
    showNotification(`New DM from ${msg.sender_tag}: "${msg.message.slice(0, 30)}..."`);
    const badge = document.getElementById("dm-unread-badge");
    const cur = parseInt(badge.innerText || "0") + 1;
    badge.innerText = cur;
    badge.style.display = "inline-block";
  }
}

// --- Friends System ---
async function loadFriends() {
  if (!state.user) {
    openAuthModal('login');
    return;
  }

  try {
    const res = await fetch("/api/friends", {
      headers: { "Authorization": `Bearer ${state.token}` }
    });
    if (res.ok) {
      const data = await res.json();
      renderFriendsList(data);
    }
  } catch (err) {
    console.error("Failed to load friends:", err);
  }
}

function renderFriendsList(data) {
  document.getElementById("friends-count").innerText = data.friends.length;

  // Pending incoming requests
  const pendingBox = document.getElementById("pending-requests-box");
  const pendingGrid = document.getElementById("pending-requests-grid");
  const friendBadge = document.getElementById("friend-req-badge");

  if (data.incoming.length > 0) {
    pendingBox.style.display = "block";
    friendBadge.innerText = data.incoming.length;
    friendBadge.style.display = "inline-block";

    pendingGrid.innerHTML = data.incoming.map(req => `
      <div style="background: var(--bg-surface); border: 1px solid var(--neon-gold); border-radius: 10px; padding: 12px; display: flex; align-items: center; justify-content: space-between;">
        <div style="display: flex; align-items: center; gap: 8px;">
          <div style="font-size: 20px;">${AVATAR_MAP[req.avatar] || '🥷'}</div>
          <div>
            <div style="font-size: 13px; font-weight: 700;">${req.gamer_tag}</div>
            <div style="font-size: 10px; color: var(--neon-cyan);">${req.primary_game} &bull; ${req.rank}</div>
          </div>
        </div>
        <div style="display: flex; gap: 6px;">
          <button onclick="acceptFriend(${req.user_id})" style="background: var(--neon-green); color: #07090e; font-size: 11px; font-weight: 700; padding: 4px 8px; border: none; border-radius: 4px; cursor: pointer;">
            ACCEPT
          </button>
          <button onclick="rejectFriend(${req.user_id})" style="background: rgba(255,255,255,0.1); color: white; font-size: 11px; padding: 4px 8px; border: none; border-radius: 4px; cursor: pointer;">
            DECLINE
          </button>
        </div>
      </div>
    `).join("");
  } else {
    pendingBox.style.display = "none";
    friendBadge.style.display = "none";
  }

  // Active Friends Grid
  const friendsGrid = document.getElementById("friends-grid");
  if (data.friends.length === 0) {
    friendsGrid.innerHTML = `
      <div style="grid-column: 1/-1; text-align: center; padding: 40px; color: var(--text-dim);">
        No friends added yet. Type a GamerTag above to connect!
      </div>
    `;
    return;
  }

  friendsGrid.innerHTML = data.friends.map(f => `
    <div style="background: var(--bg-surface); border: 1px solid var(--border-subtle); border-radius: 12px; padding: 16px; display: flex; flex-direction: column; gap: 12px;">
      <div style="display: flex; align-items: center; justify-content: space-between;">
        <div style="display: flex; align-items: center; gap: 10px;">
          <div style="font-size: 24px;">${AVATAR_MAP[f.avatar] || '🥷'}</div>
          <div>
            <div style="font-size: 14px; font-weight: 800; display: flex; align-items: center; gap: 6px;">
              <span>${f.gamer_tag}</span>
              <div class="telemetry-dot" style="width: 6px; height: 6px;"></div>
            </div>
            <div style="font-size: 11px; color: var(--text-muted);">${f.primary_game} &bull; ${f.rank}</div>
          </div>
        </div>
        <span style="font-size: 11px; color: var(--neon-green); font-weight: 700;">⭐ ${f.karma_score}</span>
      </div>

      <div style="display: flex; gap: 8px;">
        <button onclick="openDMWithUser(${f.id})" style="flex: 1; background: rgba(0, 242, 254, 0.15); border: 1px solid var(--neon-cyan); color: var(--neon-cyan); font-size: 12px; font-weight: 700; padding: 6px; border-radius: 6px; cursor: pointer;">
          <i class="fa-solid fa-message"></i> MESSAGE
        </button>
        <button onclick="removeFriend(${f.id})" style="background: rgba(255,255,255,0.05); border: 1px solid var(--border-subtle); color: var(--text-dim); font-size: 12px; padding: 6px 10px; border-radius: 6px; cursor: pointer;" title="Remove Friend">
          <i class="fa-solid fa-user-xmark"></i>
        </button>
      </div>
    </div>
  `).join("");
}

async function sendFriendRequest() {
  if (!state.user) {
    openAuthModal('login');
    return;
  }
  const input = document.getElementById("input-add-friend");
  const target = input.value.trim();
  if (!target) return;

  try {
    const res = await fetch("/api/friends/request", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "Authorization": `Bearer ${state.token}`
      },
      body: JSON.stringify({ target })
    });
    const data = await res.json();
    if (res.ok) {
      input.value = "";
      alert(data.message);
      window.audioManager.playChord();
    } else {
      alert(data.detail || "Could not send friend request");
    }
  } catch (err) {
    alert("Network error sending friend request");
  }
}

async function acceptFriend(userId) {
  try {
    const res = await fetch(`/api/friends/${userId}/accept`, {
      method: "POST",
      headers: { "Authorization": `Bearer ${state.token}` }
    });
    if (res.ok) {
      window.audioManager.playChord();
      await loadFriends();
    }
  } catch (err) {
    console.error("Failed to accept friend:", err);
  }
}

async function rejectFriend(userId) {
  try {
    await fetch(`/api/friends/${userId}/reject`, {
      method: "POST",
      headers: { "Authorization": `Bearer ${state.token}` }
    });
    await loadFriends();
  } catch (err) {
    console.error("Failed to reject friend:", err);
  }
}

async function removeFriend(userId) {
  if (confirm("Remove this player from your friends list?")) {
    await rejectFriend(userId);
  }
}

// --- Gamer Karma & Profile Card ---
let activeCardUserId = null;

async function openGamerCard(userId) {
  activeCardUserId = userId;
  try {
    const res = await fetch(`/api/users/${userId}`);
    if (res.ok) {
      const user = await res.json();
      document.getElementById("card-avatar").innerText = AVATAR_MAP[user.avatar] || "🥷";
      document.getElementById("card-gamertag").innerText = user.gamer_tag;
      document.getElementById("card-country-flag").innerText = COUNTRY_FLAGS[user.country] || "🌐";
      document.getElementById("card-rank").innerText = user.rank;
      document.getElementById("card-game").innerText = user.primary_game;
      document.getElementById("card-platform").innerText = user.platform;
      document.getElementById("card-bio").innerText = user.bio || "No bio entered yet.";
      document.getElementById("card-karma-score").innerText = `⭐ ${user.karma_score} Karma`;

      document.getElementById("modal-gamer-card").classList.add("open");
    }
  } catch (err) {
    console.error("Failed to open gamer card:", err);
  }
}

async function submitEndorsement(category) {
  if (!state.user) {
    openAuthModal('login');
    return;
  }
  if (!activeCardUserId) return;

  try {
    const res = await fetch(`/api/users/${activeCardUserId}/endorse`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "Authorization": `Bearer ${state.token}`
      },
      body: JSON.stringify({ category })
    });
    const data = await res.json();
    if (res.ok) {
      window.audioManager.playChord();
      document.getElementById("card-karma-score").innerText = `⭐ ${data.karma_score} Karma`;
      alert(data.message);
    } else {
      alert(data.detail || "Could not endorse player");
    }
  } catch (err) {
    alert("Network error endorsing player");
  }
}

function startDMFromCard() {
  if (!state.user) {
    openAuthModal('login');
    return;
  }
  closeModal('modal-gamer-card');
  openDMWithUser(activeCardUserId);
}

async function sendFriendRequestFromCard() {
  if (!state.user) {
    openAuthModal('login');
    return;
  }
  const tag = document.getElementById("card-gamertag").innerText;
  try {
    const res = await fetch("/api/friends/request", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "Authorization": `Bearer ${state.token}`
      },
      body: JSON.stringify({ target: tag })
    });
    const data = await res.json();
    if (res.ok) {
      window.audioManager.playChord();
      alert(data.message);
    } else {
      alert(data.detail || "Could not send friend request");
    }
  } catch (err) {
    alert("Network error sending friend request");
  }
}

async function loadKarmaLeaderboard() {
  const container = document.getElementById("karma-gamers-list");
  if (!container) return;

  try {
    const res = await fetch("/api/chat/us"); // fetch gamers pool
    // We can also query the top gamers from country chat or sample pool
    const pool = [
      { tag: "Kabora_KR", karma: 85, rank: "Grandmaster", game: "League of Legends", flag: "🇰🇷", avatar: "mech_warrior", title: "Korean LCK Mastermind" },
      { tag: "NordicGhost", karma: 78, rank: "Faceit Lvl 10", game: "CS2", flag: "🇸🇪", avatar: "tactical_ghost", title: "Virtus / Stockholm Legend" },
      { tag: "NeonValkyrie", karma: 62, rank: "Master", game: "Apex Legends", flag: "🇬🇧", avatar: "neon_pilot", title: "Untiltable Fast Rotator" },
      { tag: "OrangeFlashNL", karma: 58, rank: "Immortal 2", game: "Valorant", flag: "🇳🇱", avatar: "neon_pilot", title: "Amsterdam Precision Utility" },
      { tag: "SakuraBlade", karma: 54, rank: "Immortal 1", game: "Valorant", flag: "🇯🇵", avatar: "cyber_samurai", title: "Tokyo High Elo Duelist" },
      { tag: "ViperShot", karma: 48, rank: "Ascendant 3", game: "Valorant", flag: "🇺🇸", avatar: "cyber_ninja", title: "Calculated NA Shotcaller" }
    ];

    container.innerHTML = pool.map((p, idx) => `
      <div style="background: var(--bg-surface); border: 1px solid var(--border-subtle); border-radius: 12px; padding: 18px; display: flex; align-items: center; justify-content: space-between;">
        <div style="display: flex; align-items: center; gap: 12px;">
          <div style="font-size: 26px;">${AVATAR_MAP[p.avatar] || '🥷'}</div>
          <div>
            <div style="font-size: 14px; font-weight: 800; display: flex; align-items: center; gap: 6px;">
              <span>#${idx + 1} ${p.tag}</span> <span>${p.flag}</span>
            </div>
            <div style="font-size: 11px; color: var(--text-muted); margin-top: 2px;">${p.game} &bull; ${p.rank}</div>
            <div style="font-size: 11px; color: var(--text-dim); margin-top: 2px;">"${p.title}"</div>
          </div>
        </div>
        <div style="text-align: right;">
          <div style="font-size: 16px; font-weight: 800; color: var(--neon-green);">⭐ ${p.karma}</div>
          <div style="font-size: 10px; color: var(--text-dim); text-transform: uppercase;">Reputation</div>
        </div>
      </div>
    `).join("");
  } catch (err) {
    console.error("Failed to load karma leaderboard:", err);
  }
}

// --- Gamer Profile Settings ---
function loadProfileSettings() {
  if (!state.user) {
    openAuthModal('login');
    return;
  }
  const u = state.user;
  document.getElementById("profile-gamertag").value = u.gamer_tag || "";
  document.getElementById("profile-country").value = u.country || "US";
  document.getElementById("profile-primary-game").value = u.primary_game || "Valorant";
  document.getElementById("profile-rank").value = u.rank || "Diamond";
  document.getElementById("profile-platform").value = u.platform || "PC";
  document.getElementById("profile-mic").value = u.mic_status || "Always On";
  document.getElementById("profile-discord").value = u.discord_tag || "";
  document.getElementById("profile-bio").value = u.bio || "";
  document.getElementById("profile-avatar-select").value = u.avatar || "cyber_ninja";
  updateAvatarPreview();
}

function updateAvatarPreview() {
  const sel = document.getElementById("profile-avatar-select").value;
  document.getElementById("profile-avatar-preview").innerText = AVATAR_MAP[sel] || "🥷";
}

async function saveProfileChanges() {
  if (!state.user) return;

  const gamer_tag = document.getElementById("profile-gamertag").value.trim();
  const country = document.getElementById("profile-country").value;
  const primary_game = document.getElementById("profile-primary-game").value;
  const rank = document.getElementById("profile-rank").value.trim();
  const platform = document.getElementById("profile-platform").value;
  const mic_status = document.getElementById("profile-mic").value;
  const discord_tag = document.getElementById("profile-discord").value.trim();
  const bio = document.getElementById("profile-bio").value.trim();
  const avatar = document.getElementById("profile-avatar-select").value;

  try {
    const res = await fetch("/api/users/me", {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
        "Authorization": `Bearer ${state.token}`
      },
      body: JSON.stringify({
        gamer_tag, country, primary_game, rank, platform, mic_status, discord_tag, bio, avatar
      })
    });
    if (res.ok) {
      state.user = await res.json();
      renderAuthNav(state.user);
      window.audioManager.playChord();
      alert("Gamer Profile updated successfully!");
    } else {
      alert("Failed to update profile");
    }
  } catch (err) {
    alert("Network error updating profile");
  }
}

// --- Utilities ---
function closeModal(modalId) {
  const m = document.getElementById(modalId);
  if (m) m.classList.remove("open");
}

function escapeHTML(str) {
  if (!str) return "";
  return str.replace(/[&<>'"]/g, 
    tag => ({
      '&': '&amp;',
      '<': '&lt;',
      '>': '&gt;',
      "'": '&#39;',
      '"': '&quot;'
    }[tag] || tag)
  );
}

function showNotification(text) {
  const div = document.createElement("div");
  div.style.position = "fixed";
  div.style.bottom = "24px";
  div.style.right = "24px";
  div.style.background = "var(--bg-elevated)";
  div.style.border = "1px solid var(--neon-cyan)";
  div.style.color = "white";
  div.style.padding = "12px 20px";
  div.style.borderRadius = "10px";
  div.style.boxShadow = "0 10px 30px rgba(0,0,0,0.8), 0 0 15px rgba(0,242,254,0.3)";
  div.style.fontSize = "13px";
  div.style.fontWeight = "600";
  div.style.zIndex = "999";
  div.style.animation = "fadeIn 0.2s ease";
  div.innerText = text;
  document.body.appendChild(div);

  setTimeout(() => {
    div.style.opacity = "0";
    div.style.transition = "opacity 0.3s ease";
    setTimeout(() => div.remove(), 300);
  }, 4000);
}

// --- Gaming Guides & SEO/LLM Blog Hub ---
async function loadBlogArticles() {
  try {
    const res = await fetch("/api/blogs");
    if (res.ok) {
      state.blogsList = await res.json();
      filterBlogsLocally();
    }
  } catch (err) {
    console.error("Failed to load blog articles:", err);
  }
}

function filterBlogCategory(cat) {
  state.selectedBlogCategory = cat;
  state.selectedBlogGame = "All Games";
  updateBlogPillsUI();
  filterBlogsLocally();
}

function filterBlogGame(game) {
  state.selectedBlogGame = game;
  state.selectedBlogCategory = "All";
  updateBlogPillsUI();
  filterBlogsLocally();
}

function updateBlogPillsUI() {
  const pills = document.querySelectorAll("#blog-categories-pills .country-chip");
  pills.forEach(p => p.classList.remove("active"));

  if (state.selectedBlogCategory !== "All") {
    if (state.selectedBlogCategory === "Top 15") document.getElementById("pill-top15")?.classList.add("active");
    else if (state.selectedBlogCategory === "Top 12") document.getElementById("pill-top12")?.classList.add("active");
    else if (state.selectedBlogCategory === "Top 10") document.getElementById("pill-top10")?.classList.add("active");
  } else if (state.selectedBlogGame !== "All Games") {
    if (state.selectedBlogGame === "Minecraft") document.getElementById("pill-mc")?.classList.add("active");
    else if (state.selectedBlogGame === "Roblox") document.getElementById("pill-roblox")?.classList.add("active");
    else if (state.selectedBlogGame === "Warzone") document.getElementById("pill-cod")?.classList.add("active");
    else if (state.selectedBlogGame === "Fortnite") document.getElementById("pill-fn")?.classList.add("active");
  } else {
    document.getElementById("pill-all")?.classList.add("active");
  }
}

function filterBlogsLocally() {
  const q = (document.getElementById("search-blogs")?.value || "").toLowerCase().trim();
  let filtered = state.blogsList || [];

  if (state.selectedBlogCategory && state.selectedBlogCategory !== "All") {
    filtered = filtered.filter(b => b.category.toLowerCase() === state.selectedBlogCategory.toLowerCase());
  }

  if (state.selectedBlogGame && state.selectedBlogGame !== "All Games") {
    filtered = filtered.filter(b => b.game_tag.toLowerCase() === state.selectedBlogGame.toLowerCase() || b.game_tag === "All Games");
  }

  if (q) {
    filtered = filtered.filter(b => 
      b.title.toLowerCase().includes(q) ||
      b.meta_description.toLowerCase().includes(q) ||
      (b.target_keywords && b.target_keywords.some(k => k.toLowerCase().includes(q))) ||
      (b.llm_summary && b.llm_summary.toLowerCase().includes(q))
    );
  }

  renderBlogGrid(filtered);
}

function renderBlogGrid(articles) {
  const container = document.getElementById("blogs-container");
  if (!container) return;

  if (!articles || articles.length === 0) {
    container.innerHTML = `
      <div style="grid-column: 1/-1; text-align: center; padding: 60px 20px; color: var(--text-dim);">
        <i class="fa-solid fa-book-open fa-3x" style="margin-bottom: 16px; opacity: 0.4;"></i>
        <h3 style="font-size: 18px; color: var(--text-muted); margin-bottom: 8px;">No Guides Found</h3>
        <p style="font-size: 13px;">Try selecting another category or clear your search filter.</p>
        <button class="country-chip active" onclick="filterBlogCategory('All')" style="margin: 16px auto 0;">View All Guides</button>
      </div>
    `;
    return;
  }

  container.innerHTML = articles.map(a => `
    <div class="blog-card" onclick="viewBlogArticle('${a.slug}')">
      <div style="display: flex; justify-content: space-between; align-items: flex-start;">
        <span class="blog-badge">${a.banner_badge}</span>
        <span style="font-size: 11px; color: var(--neon-cyan); background: rgba(0, 242, 254, 0.08); padding: 3px 8px; border-radius: 4px; font-weight: 700;">
          ${a.game_tag}
        </span>
      </div>

      <h2 class="blog-card-title">${escapeHTML(a.title)}</h2>
      <p class="blog-card-desc">${escapeHTML(a.meta_description)}</p>

      <div style="background: rgba(0,0,0,0.25); border-left: 3px solid var(--neon-cyan); padding: 10px 12px; border-radius: 6px; margin-bottom: 16px;">
        <div style="font-size: 11px; font-weight: 800; color: var(--neon-cyan); margin-bottom: 4px; text-transform: uppercase;">
          <i class="fa-solid fa-robot"></i> LLM Summary Preview
        </div>
        <div style="font-size: 12px; color: var(--text-muted); line-height: 1.4; display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden;">
          ${escapeHTML(a.llm_summary)}
        </div>
      </div>

      <div style="display: flex; flex-wrap: wrap; gap: 4px; margin-bottom: 16px;">
        ${(a.target_keywords || []).slice(0, 3).map(k => `
          <span style="font-size: 10px; background: rgba(255,255,255,0.05); color: var(--text-muted); padding: 2px 6px; border-radius: 4px;">#${escapeHTML(k)}</span>
        `).join("")}
      </div>

      <div class="blog-card-footer">
        <div>
          <span style="color: var(--text-main); font-weight: 700;">${escapeHTML(a.author)}</span>
          <span style="margin: 0 4px;">&bull;</span>
          <span>${a.read_time}</span>
        </div>
        <span style="color: var(--neon-cyan); font-weight: 700; display: flex; align-items: center; gap: 6px;">
          READ GUIDE <i class="fa-solid fa-arrow-right fa-xs"></i>
        </span>
      </div>
    </div>
  `).join("");
}

async function viewBlogArticle(slug) {
  try {
    const res = await fetch(`/api/blogs/${slug}`);
    if (!res.ok) {
      alert("Failed to load article");
      return;
    }
    const data = await res.json();
    const article = data.article || data;
    state.activeBlogArticle = article;

    // Populate Reader View elements
    document.getElementById("reader-badge").innerText = article.banner_badge;
    document.getElementById("reader-title").innerText = article.title;
    document.getElementById("reader-author").innerText = article.author;
    document.getElementById("reader-date").innerText = article.published_at;
    document.getElementById("reader-readtime").innerText = article.read_time;
    document.getElementById("reader-body").innerHTML = article.content_html;

    const squadBtnText = document.getElementById("reader-btn-find-squad-text");
    if (squadBtnText) {
      const tag = article.game_tag === "All Games" ? "COMPETITIVE" : article.game_tag.toUpperCase();
      squadBtnText.innerText = `FIND A SQUAD FOR ${tag}`;
    }

    // Inject/Update dynamic Schema.org JSON-LD tag for search engine bots & LLMs
    let jsonLdScript = document.getElementById("article-json-ld");
    if (!jsonLdScript) {
      jsonLdScript = document.createElement("script");
      jsonLdScript.id = "article-json-ld";
      jsonLdScript.type = "application/ld+json";
      document.head.appendChild(jsonLdScript);
    }
    if (article.schema_data) {
      jsonLdScript.text = JSON.stringify(article.schema_data);
    }

    // Toggle views
    document.getElementById("blog-grid-view").style.display = "none";
    document.getElementById("blog-reader-view").style.display = "block";

    // Play click sound and scroll to top
    window.audioManager.playClick();
    const mainView = document.querySelector(".main-view");
    if (mainView) mainView.scrollTop = 0;
    else window.scrollTo({ top: 0, behavior: "smooth" });

  } catch (err) {
    console.error("Failed to fetch article:", err);
    alert("Network error loading article");
  }
}

function backToBlogList() {
  document.getElementById("blog-reader-view").style.display = "none";
  document.getElementById("blog-grid-view").style.display = "block";
  window.audioManager.playClick();
}

function findSquadForArticleGame() {
  if (!state.activeBlogArticle) return;
  const game = state.activeBlogArticle.game_tag;

  // Switch to Squads tab
  switchTab("squads");

  // Select game filter if applicable
  const filterSelect = document.getElementById("filter-game");
  if (filterSelect && game && game !== "All Games") {
    for (let opt of filterSelect.options) {
      if (opt.value.toLowerCase() === game.toLowerCase() || opt.text.toLowerCase().includes(game.toLowerCase())) {
        filterSelect.value = opt.value;
        break;
      }
    }
  } else if (filterSelect) {
    filterSelect.value = "All Games";
  }
  loadSquads();
}
