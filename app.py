import streamlit as st
import pandas as pd
import os
from datetime import datetime, date, timedelta
import json
import hashlib

# ─── PAGE CONFIG ────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Crossfit med Odin 🏋️",
    page_icon="🏋️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ─── CUSTOM CSS ─────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Inter:wght@300;400;600;700&display=swap');

:root {
    --orange: #FF4D00;
    --dark:   #0D0D0D;
    --card:   #1A1A1A;
    --border: #2A2A2A;
    --text:   #F0F0F0;
    --muted:  #888888;
}

html, body, [data-testid="stAppViewContainer"] {
    background-color: var(--dark) !important;
    color: var(--text) !important;
    font-family: 'Inter', sans-serif;
}

[data-testid="stHeader"] { background: transparent !important; }

h1, h2, h3 {
    font-family: 'Bebas Neue', sans-serif !important;
    letter-spacing: 2px;
    color: var(--text) !important;
}

.hero {
    background: linear-gradient(135deg, #FF4D00 0%, #FF8C00 60%, #1A1A1A 100%);
    border-radius: 16px;
    padding: 48px 40px;
    margin-bottom: 32px;
    position: relative;
    overflow: hidden;
}
.hero::before {
    content: "ODIN";
    position: absolute;
    right: -20px; top: -20px;
    font-family: 'Bebas Neue', sans-serif;
    font-size: 180px;
    color: rgba(255,255,255,0.07);
    line-height: 1;
    pointer-events: none;
}
.hero h1 { font-size: 56px !important; color: white !important; margin: 0; }
.hero p  { color: rgba(255,255,255,0.85); font-size: 18px; margin: 8px 0 0; }

.card {
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 24px;
    margin-bottom: 16px;
}
.card h3 { font-size: 22px; margin-bottom: 16px; }

.badge-orange {
    display: inline-block;
    background: var(--orange);
    color: white;
    font-weight: 700;
    font-size: 12px;
    letter-spacing: 1px;
    padding: 3px 10px;
    border-radius: 20px;
    text-transform: uppercase;
    margin-bottom: 8px;
}

.badge-trainer {
    display: inline-block;
    background: #2E7D32;
    color: white;
    font-weight: 700;
    font-size: 11px;
    letter-spacing: 1px;
    padding: 3px 10px;
    border-radius: 20px;
    text-transform: uppercase;
}

.stat-box {
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 20px;
    text-align: center;
}
.stat-box .number {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 52px;
    color: var(--orange);
    line-height: 1;
}
.stat-box .label {
    font-size: 12px;
    color: var(--muted);
    text-transform: uppercase;
    letter-spacing: 1px;
    margin-top: 4px;
}

.leaderboard-row {
    display: flex;
    align-items: center;
    gap: 16px;
    padding: 14px 0;
    border-bottom: 1px solid var(--border);
}
.leaderboard-row:last-child { border-bottom: none; }
.rank {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 28px;
    color: var(--muted);
    width: 32px;
    text-align: center;
}
.rank.gold   { color: #FFD700; }
.rank.silver { color: #C0C0C0; }
.rank.bronze { color: #CD7F32; }
.lb-name  { font-weight: 600; flex: 1; }
.lb-count {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 24px;
    color: var(--orange);
}
.lb-bar-wrap { width: 100px; background: var(--border); border-radius: 4px; height: 6px; }
.lb-bar { background: var(--orange); height: 6px; border-radius: 4px; }

.signup-pill {
    display: inline-block;
    background: #1F2F1F;
    border: 1px solid #2E4D2E;
    color: #7DDE7D;
    border-radius: 20px;
    padding: 6px 14px;
    font-size: 14px;
    font-weight: 600;
    margin: 4px 4px 4px 0;
}

.wod-text {
    background: #111;
    border-left: 4px solid var(--orange);
    border-radius: 0 8px 8px 0;
    padding: 16px 20px;
    font-family: 'Inter', sans-serif;
    font-size: 15px;
    line-height: 1.8;
    white-space: pre-wrap;
    color: var(--text);
}

.stButton > button {
    background: var(--orange) !important;
    color: white !important;
    border: none !important;
    font-family: 'Bebas Neue', sans-serif !important;
    font-size: 20px !important;
    letter-spacing: 2px !important;
    border-radius: 8px !important;
    padding: 10px 32px !important;
    width: 100%;
    transition: opacity 0.2s;
}
.stButton > button:hover { opacity: 0.85 !important; }

.stTextInput > div > div > input,
.stTextArea > div > div > textarea,
.stSelectbox > div > div {
    background: #111 !important;
    border: 1px solid var(--border) !important;
    color: var(--text) !important;
    border-radius: 8px !important;
}
.stTextInput label, .stTextArea label, .stSelectbox label,
.stDateInput label, .stCheckbox label {
    color: var(--muted) !important;
    font-size: 13px !important;
    letter-spacing: 0.5px !important;
    text-transform: uppercase !important;
}

[data-testid="stSidebar"] {
    background: var(--card) !important;
    border-right: 1px solid var(--border) !important;
}

div[data-testid="stSuccessMessage"] { border-radius: 8px; }
div[data-testid="stErrorMessage"]   { border-radius: 8px; }

hr { border-color: var(--border) !important; }

/* ─── MOBILE RESPONSIVE ─── */
@media (max-width: 768px) {
    .hero {
        padding: 28px 20px;
        border-radius: 10px;
    }
    .hero h1 { font-size: 32px !important; }
    .hero p  { font-size: 14px; }
    .hero::before { font-size: 100px; }

    .stat-box { padding: 14px 10px; }
    .stat-box .number { font-size: 36px; }
    .stat-box .label  { font-size: 10px; }

    .card { padding: 16px; border-radius: 10px; }
    .card h3 { font-size: 18px; }

    .leaderboard-row { gap: 10px; padding: 10px 0; }
    .rank { font-size: 22px; width: 26px; }
    .lb-count { font-size: 20px; }
    .lb-bar-wrap { width: 60px; }

    .wod-text { padding: 12px 14px; font-size: 14px; }
}
</style>
""", unsafe_allow_html=True)

# ─── DATA FILES ─────────────────────────────────────────────────────────────
SIGNUPS_FILE = "signups.csv"
WOD_FILE     = "wods.json"
USERS_FILE   = "users.json"

# ─── USER / AUTH HELPERS ────────────────────────────────────────────────────

def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode("utf-8")).hexdigest()

def load_users() -> dict:
    if os.path.exists(USERS_FILE):
        try:
            with open(USERS_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {}
    return {}

def save_users(users: dict):
    with open(USERS_FILE, "w", encoding="utf-8") as f:
        json.dump(users, f, indent=2, ensure_ascii=False)

def seed_trainer():
    users = load_users()
    if "odin" not in users:
        users["odin"] = {
            "display_name": "Odin",
            "password_hash": hash_password("odin2026"),
            "role": "trainer",
            "created": datetime.now().isoformat(),
        }
        save_users(users)

def register_user(username: str, display_name: str, password: str) -> str | None:
    """Register a new user. Returns error message or None on success."""
    username = username.strip().lower()
    if not username:
        return "Brukernavn kan ikke være tomt"
    if not display_name.strip():
        return "Fullt navn kan ikke være tomt"
    if len(password) < 4:
        return "Passord må være minst 4 tegn"

    users = load_users()
    if username in users:
        return "Brukernavnet er allerede tatt"

    users[username] = {
        "display_name": display_name.strip(),
        "password_hash": hash_password(password),
        "role": "user",
        "created": datetime.now().isoformat(),
    }
    save_users(users)
    return None

def authenticate(username: str, password: str) -> dict | None:
    """Authenticate user. Returns user dict or None."""
    users = load_users()
    user = users.get(username.strip().lower())
    if user and user["password_hash"] == hash_password(password):
        return user
    return None

def is_trainer(username: str) -> bool:
    users = load_users()
    user = users.get(username.strip().lower())
    return user is not None and user.get("role") == "trainer"

# Seed trainer account on startup
seed_trainer()

# ─── DATA HELPERS ────────────────────────────────────────────────────────────

def load_signups() -> pd.DataFrame:
    if os.path.exists(SIGNUPS_FILE):
        try:
            df = pd.read_csv(SIGNUPS_FILE)
            if df.empty or not {"name", "date"}.issubset(df.columns):
                return _empty_signups()
            return df
        except Exception:
            return _empty_signups()
    return _empty_signups()

def _empty_signups():
    return pd.DataFrame(columns=["name", "date"])

def save_signup(name: str, session_date: str):
    df = load_signups()
    new_row = pd.DataFrame([{"name": name.strip(), "date": session_date}])
    df = pd.concat([df, new_row], ignore_index=True)
    df.to_csv(SIGNUPS_FILE, index=False)

def is_signed_up(name: str, session_date: str) -> bool:
    df = load_signups()
    return not df[(df["name"].str.lower() == name.strip().lower()) & (df["date"] == session_date)].empty

def remove_signup(name: str, session_date: str):
    df = load_signups()
    df = df[~((df["name"].str.lower() == name.strip().lower()) & (df["date"] == session_date))]
    df.to_csv(SIGNUPS_FILE, index=False)

def load_wods() -> dict:
    if os.path.exists(WOD_FILE):
        try:
            with open(WOD_FILE, "r") as f:
                return json.load(f)
        except Exception:
            return {}
    return {}

def save_wod(session_date: str, wod_text: str, trainer_name: str):
    wods = load_wods()
    wods[session_date] = {"wod": wod_text, "added_by": trainer_name, "updated": datetime.now().isoformat()}
    with open(WOD_FILE, "w") as f:
        json.dump(wods, f, indent=2)

# ─── NEXT FRIDAY ─────────────────────────────────────────────────────────────
def next_friday() -> date:
    today = date.today()
    days_ahead = 4 - today.weekday()  # Friday is weekday 4
    if days_ahead < 0:
        days_ahead += 7
    return today + timedelta(days=days_ahead)

# ─── SESSION STATE ───────────────────────────────────────────────────────────
if "username" not in st.session_state:
    st.session_state.username = ""
if "display_name" not in st.session_state:
    st.session_state.display_name = ""

# ─── SIDEBAR: LOGIN / REGISTER ──────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🏋️ Crossfit med Odin")
    st.markdown("---")

    if not st.session_state.username:
        tab_login, tab_register = st.tabs(["Logg inn", "Registrer deg"])

        with tab_login:
            login_user = st.text_input("Brukernavn", placeholder="f.eks. robin", key="login_user")
            login_pwd = st.text_input("Passord", type="password", key="login_pwd")
            if st.button("Logg inn", key="btn_login"):
                user = authenticate(login_user, login_pwd)
                if user:
                    st.session_state.username = login_user.strip().lower()
                    st.session_state.display_name = user["display_name"]
                    st.rerun()
                else:
                    st.error("Feil brukernavn eller passord")

        with tab_register:
            reg_name = st.text_input("Fullt navn", placeholder="Ola Nordmann", key="reg_name")
            reg_user = st.text_input("Velg brukernavn", placeholder="ola", key="reg_user")
            reg_pwd = st.text_input("Passord", type="password", key="reg_pwd")
            reg_pwd2 = st.text_input("Bekreft passord", type="password", key="reg_pwd2")
            if st.button("Opprett konto", key="btn_register"):
                if reg_pwd != reg_pwd2:
                    st.error("Passordene er ikke like")
                else:
                    err = register_user(reg_user, reg_name, reg_pwd)
                    if err:
                        st.error(err)
                    else:
                        st.session_state.username = reg_user.strip().lower()
                        st.session_state.display_name = reg_name.strip()
                        st.success("Konto opprettet!")
                        st.rerun()
    else:
        st.markdown(f"**Logget inn som:**")
        trainer = is_trainer(st.session_state.username)
        if trainer:
            st.markdown(f'### {st.session_state.display_name} <span class="badge-trainer">Trener</span>', unsafe_allow_html=True)
        else:
            st.markdown(f"### {st.session_state.display_name}")
        if st.button("Logg ut"):
            st.session_state.username = ""
            st.session_state.display_name = ""
            st.rerun()

# ─── MAIN CONTENT ────────────────────────────────────────────────────────────
friday = next_friday()
friday_str = friday.strftime("%Y-%m-%d")
friday_display = friday.strftime("%d. %B %Y").replace(
    "January","januar").replace("February","februar").replace("March","mars").replace(
    "April","april").replace("May","mai").replace("June","juni").replace(
    "July","juli").replace("August","august").replace("September","september").replace(
    "October","oktober").replace("November","november").replace("December","desember")

# HERO
st.markdown(f"""
<div class="hero">
    <h1>CROSSFIT MED ODIN 🔥</h1>
    <p>Neste økt: Fredag {friday_display}</p>
</div>
""", unsafe_allow_html=True)

# ─── GATE: Ikke logget inn ───────────────────────────────────────────────────
if not st.session_state.username:
    st.info("👈 Logg inn eller registrer deg i sidepanelet for å komme i gang!")
    df = load_signups()
    wods = load_wods()
    # Vis bare leaderboard for besøkende
    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown('<div class="card"><h3>🏆 Leaderboard — Alle tider</h3>', unsafe_allow_html=True)
        if not df.empty:
            counts = df.groupby("name").size().reset_index(name="count").sort_values("count", ascending=False)
            max_c = counts["count"].max() if not counts.empty else 1
            medals = ["gold", "silver", "bronze"]
            html = ""
            for i, row in counts.head(10).iterrows():
                rank_i  = list(counts.index).index(i) + 1
                medal   = medals[rank_i - 1] if rank_i <= 3 else ""
                pct     = int(row["count"] / max_c * 100)
                html += f"""
                <div class="leaderboard-row">
                    <div class="rank {medal}">#{rank_i}</div>
                    <div class="lb-name">{row['name']}</div>
                    <div class="lb-bar-wrap"><div class="lb-bar" style="width:{pct}%"></div></div>
                    <div class="lb-count">{row['count']}</div>
                </div>"""
            st.markdown(html, unsafe_allow_html=True)
        else:
            st.markdown("*Ingen treninger registrert ennå*")
        st.markdown("</div>", unsafe_allow_html=True)
    st.stop()

# ─── LOGGED IN ───────────────────────────────────────────────────────────────
df   = load_signups()
wods = load_wods()

signed_up   = is_signed_up(st.session_state.display_name, friday_str)
signups_today = df[df["date"] == friday_str] if not df.empty else pd.DataFrame()
total_sessions = len(df[df["name"].str.lower() == st.session_state.display_name.lower()]) if not df.empty else 0

# ── STATS ROW ──
c1, c2, c3 = st.columns(3)
with c1:
    st.markdown(f"""
    <div class="stat-box">
        <div class="number">{len(signups_today)}</div>
        <div class="label">Påmeldt fredag</div>
    </div>""", unsafe_allow_html=True)
with c2:
    st.markdown(f"""
    <div class="stat-box">
        <div class="number">{total_sessions}</div>
        <div class="label">Dine treninger</div>
    </div>""", unsafe_allow_html=True)
with c3:
    total_all = len(df["date"].unique()) if not df.empty else 0
    st.markdown(f"""
    <div class="stat-box">
        <div class="number">{total_all}</div>
        <div class="label">Totalt økter</div>
    </div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── MAIN 2-COL LAYOUT ──
left, right = st.columns([1, 1], gap="large")

# LEFT: Påmelding + WOD
with left:
    # Påmelding
    st.markdown(f'<div class="card"><h3>📅 Fredag {friday_display}</h3>', unsafe_allow_html=True)

    wod_info = wods.get(friday_str)
    if wod_info:
        st.markdown(f'<span class="badge-orange">Dagens økt er klar!</span>', unsafe_allow_html=True)
        st.markdown(f'<div class="wod-text">{wod_info["wod"]}</div>', unsafe_allow_html=True)
        st.markdown(f'<p style="color:#555;font-size:12px;margin-top:8px">Lagt inn av {wod_info.get("added_by","trener")}</p>', unsafe_allow_html=True)
    else:
        st.markdown('*WOD ikke lagt inn ennå – kom tilbake snart!*')

    st.markdown("<br>", unsafe_allow_html=True)

    if signed_up:
        st.success(f"✅ Du er påmeldt!")
        if st.button("Meld meg av"):
            remove_signup(st.session_state.display_name, friday_str)
            st.rerun()
    else:
        if st.button("🔥 MELD MEG PÅ"):
            save_signup(st.session_state.display_name, friday_str)
            st.balloons()
            st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)

    # Påmeldte denne uken
    if not signups_today.empty:
        st.markdown('<div class="card"><h3>💪 Påmeldte denne uken</h3>', unsafe_allow_html=True)
        pills = "".join([f'<span class="signup-pill">✓ {n}</span>' for n in signups_today["name"].tolist()])
        st.markdown(pills, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

# RIGHT: Leaderboard + Historikk
with right:
    # Leaderboard
    st.markdown('<div class="card"><h3>🏆 Leaderboard</h3>', unsafe_allow_html=True)
    if not df.empty:
        counts = df.groupby("name").size().reset_index(name="count").sort_values("count", ascending=False)
        max_c = counts["count"].max()
        medals = ["gold", "silver", "bronze"]
        html = ""
        for rank_i, (_, row) in enumerate(counts.head(10).iterrows(), 1):
            medal = medals[rank_i - 1] if rank_i <= 3 else ""
            pct   = int(row["count"] / max_c * 100)
            you   = " 👈" if row["name"].lower() == st.session_state.display_name.lower() else ""
            html += f"""
            <div class="leaderboard-row">
                <div class="rank {medal}">#{rank_i}</div>
                <div class="lb-name">{row['name']}{you}</div>
                <div class="lb-bar-wrap"><div class="lb-bar" style="width:{pct}%"></div></div>
                <div class="lb-count">{row['count']}</div>
            </div>"""
        st.markdown(html, unsafe_allow_html=True)
    else:
        st.markdown("*Ingen data ennå – vær den første!*")
    st.markdown("</div>", unsafe_allow_html=True)

    # Siste 5 økter
    st.markdown('<div class="card"><h3>📋 Siste økter</h3>', unsafe_allow_html=True)
    if not df.empty:
        recent_dates = sorted(df["date"].unique(), reverse=True)[:5]
        for d in recent_dates:
            count = len(df[df["date"] == d])
            d_fmt = datetime.strptime(d, "%Y-%m-%d").strftime("%d.%m.%Y")
            wod_d = wods.get(d, {}).get("wod", "")
            preview = (wod_d[:50] + "…") if len(wod_d) > 50 else (wod_d or "*Ingen WOD registrert*")
            st.markdown(f"""
            <div style="padding:10px 0;border-bottom:1px solid var(--border)">
                <div style="font-weight:700">{d_fmt} <span style="color:var(--muted);font-size:13px">· {count} deltakere</span></div>
                <div style="color:var(--muted);font-size:13px;margin-top:2px">{preview}</div>
            </div>""", unsafe_allow_html=True)
    else:
        st.markdown("*Ingen historikk ennå*")
    st.markdown("</div>", unsafe_allow_html=True)

# ─── TRENER-PANEL ───────────────────────────────────────────────────────────
if is_trainer(st.session_state.username):
    st.markdown("---")
    st.markdown("## 🏋️ Trener-panel")
    a1, a2 = st.columns(2)

    with a1:
        st.markdown('<div class="card"><h3>📝 Legg inn WOD</h3>', unsafe_allow_html=True)
        wod_date = st.date_input("Dato for økt", value=friday, key="wod_date")
        wod_text = st.text_area("Dagens WOD", height=180,
            placeholder="Eks:\n21-15-9\nThrusters 42.5/30 kg\nPull-ups\n\nFor tid ⏱️",
            value=wods.get(str(wod_date), {}).get("wod", ""))
        if st.button("💾 Lagre WOD"):
            if wod_text.strip():
                save_wod(str(wod_date), wod_text.strip(), st.session_state.display_name)
                st.success("WOD lagret!")
                st.rerun()
            else:
                st.error("Skriv inn WOD-tekst")
        st.markdown("</div>", unsafe_allow_html=True)

    with a2:
        st.markdown('<div class="card"><h3>🗂️ Administrer påmeldinger</h3>', unsafe_allow_html=True)
        manage_date = st.date_input("Velg dato", value=friday, key="manage_date")
        day_df = df[df["date"] == str(manage_date)] if not df.empty else pd.DataFrame()

        if not day_df.empty:
            st.markdown(f"**{len(day_df)} deltakere registrert**")
            for _, row in day_df.iterrows():
                col_n, col_x = st.columns([4, 1])
                col_n.write(row["name"])
                if col_x.button("✕", key=f"del_{row['name']}_{row['date']}"):
                    remove_signup(row["name"], str(manage_date))
                    st.rerun()
        else:
            st.info("Ingen påmeldte denne dagen")

        st.markdown("**➕ Legg til deltaker manuelt**")
        manual_name = st.text_input("Navn", key="manual_name")
        if st.button("Legg til"):
            if manual_name.strip():
                if not is_signed_up(manual_name, str(manage_date)):
                    save_signup(manual_name, str(manage_date))
                    st.success(f"{manual_name} lagt til!")
                    st.rerun()
                else:
                    st.warning("Allerede påmeldt")
        st.markdown("</div>", unsafe_allow_html=True)

    # Full data export
    st.markdown('<div class="card"><h3>📊 Alle data</h3>', unsafe_allow_html=True)
    if not df.empty:
        st.dataframe(df.sort_values("date", ascending=False), use_container_width=True)
        csv = df.to_csv(index=False).encode("utf-8")
        st.download_button("⬇️ Last ned CSV", csv, "crossfit_data.csv", "text/csv")
    else:
        st.info("Ingen data ennå")
    st.markdown("</div>", unsafe_allow_html=True)
