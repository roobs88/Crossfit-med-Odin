import streamlit as st
import pandas as pd
import os
from datetime import datetime, date, timedelta
import json
import hashlib

# ─── CONFIG ─────────────────────────────────────────────────────────────────
TRAINER_PIN = "2026"

# ─── PAGE CONFIG ────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Crossfit med Malde",
    page_icon="🏋️",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ─── CUSTOM CSS ─────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Inter:wght@300;400;600;700&display=swap');

:root {
    --accent: #00875A;
    --accent-light: #00A86B;
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
    background: linear-gradient(135deg, #00875A 0%, #00A86B 50%, #1A1A1A 100%);
    border-radius: 16px;
    padding: 48px 40px;
    margin-bottom: 32px;
    position: relative;
    overflow: hidden;
}
.hero::before {
    content: "MALDE";
    position: absolute;
    right: -20px; top: -20px;
    font-family: 'Bebas Neue', sans-serif;
    font-size: 160px;
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
    padding: 28px;
    margin-bottom: 20px;
    box-shadow: 0 4px 24px rgba(0,0,0,0.3);
}
.card h3 { font-size: 22px; margin-bottom: 16px; }

.badge-orange {
    display: inline-block;
    background: var(--accent);
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
    color: var(--accent);
}
.lb-bar-wrap { width: 100px; background: var(--border); border-radius: 4px; height: 6px; }
.lb-bar { background: var(--accent); height: 6px; border-radius: 4px; }

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
    border-left: 4px solid var(--accent);
    border-radius: 0 8px 8px 0;
    padding: 16px 20px;
    font-family: 'Inter', sans-serif;
    font-size: 15px;
    line-height: 1.8;
    white-space: pre-wrap;
    color: var(--text);
}

.welcome-text {
    color: var(--muted);
    font-size: 16px;
    line-height: 1.6;
    text-align: center;
    margin: 0 auto 24px;
    max-width: 500px;
}

.stButton > button {
    background: var(--accent) !important;
    color: white !important;
    border: none !important;
    font-family: 'Bebas Neue', sans-serif !important;
    font-size: 20px !important;
    letter-spacing: 2px !important;
    border-radius: 8px !important;
    padding: 12px 32px !important;
    width: 100%;
    transition: all 0.2s ease;
    box-shadow: 0 4px 16px rgba(0,135,90,0.3);
}
.stButton > button:hover {
    opacity: 0.9 !important;
    box-shadow: 0 6px 24px rgba(0,135,90,0.45) !important;
    transform: translateY(-1px);
}

.btn-secondary > button {
    background: transparent !important;
    border: 2px solid var(--border) !important;
    color: var(--text) !important;
    box-shadow: none !important;
}
.btn-secondary > button:hover {
    border-color: var(--accent) !important;
    box-shadow: none !important;
}

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

    .card { padding: 18px; border-radius: 10px; }
    .card h3 { font-size: 18px; }

    .leaderboard-row { gap: 10px; padding: 10px 0; }
    .rank { font-size: 22px; width: 26px; }
    .lb-count { font-size: 20px; }
    .lb-bar-wrap { width: 60px; }

    .wod-text { padding: 12px 14px; font-size: 14px; }

    .welcome-text { font-size: 14px; }
}
</style>
""", unsafe_allow_html=True)

# ─── DATA FILES ─────────────────────────────────────────────────────────────
SIGNUPS_FILE = "signups.csv"
WOD_FILE     = "wods.json"

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
if "display_name" not in st.session_state:
    st.session_state.display_name = ""
if "is_trainer" not in st.session_state:
    st.session_state.is_trainer = False

# ─── DATE SETUP ──────────────────────────────────────────────────────────────
friday = next_friday()
friday_str = friday.strftime("%Y-%m-%d")
friday_display = friday.strftime("%d. %B %Y").replace(
    "January","januar").replace("February","februar").replace("March","mars").replace(
    "April","april").replace("May","mai").replace("June","juni").replace(
    "July","juli").replace("August","august").replace("September","september").replace(
    "October","oktober").replace("November","november").replace("December","desember")

# ─── HERO ────────────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="hero">
    <h1>CROSSFIT MED MALDE</h1>
    <p>Neste økt: Fredag {friday_display}</p>
</div>
""", unsafe_allow_html=True)

# ─── HELPER: RENDER LEADERBOARD ─────────────────────────────────────────────
def render_leaderboard(df, highlight_name=None):
    st.markdown('<div class="card"><h3>Leaderboard</h3>', unsafe_allow_html=True)
    if not df.empty:
        counts = df.groupby("name").size().reset_index(name="count").sort_values("count", ascending=False)
        max_c = counts["count"].max() if not counts.empty else 1
        medals = ["gold", "silver", "bronze"]
        html = ""
        for rank_i, (_, row) in enumerate(counts.head(10).iterrows(), 1):
            medal = medals[rank_i - 1] if rank_i <= 3 else ""
            pct = int(row["count"] / max_c * 100)
            you = " — deg" if highlight_name and row["name"].lower() == highlight_name.lower() else ""
            html += f"""
            <div class="leaderboard-row">
                <div class="rank {medal}">#{rank_i}</div>
                <div class="lb-name">{row['name']}{you}</div>
                <div class="lb-bar-wrap"><div class="lb-bar" style="width:{pct}%"></div></div>
                <div class="lb-count">{row['count']}</div>
            </div>"""
        st.markdown(html, unsafe_allow_html=True)
    else:
        st.markdown("*Ingen treninger registrert ennå — vær den første!*")
    st.markdown("</div>", unsafe_allow_html=True)

# ═════════════════════════════════════════════════════════════════════════════
# NOT REGISTERED — Welcome + Name input + Leaderboard
# ═════════════════════════════════════════════════════════════════════════════
if not st.session_state.display_name:

    st.markdown("""
    <p class="welcome-text">
        Meld deg på fredagens CrossFit-økt med Christian!<br>
        Skriv inn navnet ditt for å komme i gang.
    </p>
    """, unsafe_allow_html=True)

    name_input = st.text_input("Ditt navn", placeholder="F.eks. Ola Nordmann", key="name_input")
    if st.button("Kom i gang", key="btn_enter"):
        if name_input.strip():
            st.session_state.display_name = name_input.strip()
            st.rerun()
        else:
            st.error("Skriv inn navnet ditt")

    st.markdown("<br>", unsafe_allow_html=True)

    # Leaderboard visible for motivation
    df = load_signups()
    render_leaderboard(df)

    st.stop()

# ═════════════════════════════════════════════════════════════════════════════
# REGISTERED / ACTIVE USER
# ═════════════════════════════════════════════════════════════════════════════

# ─── SIDEBAR: Profile + Trainer toggle + Sign out ────────────────────────────
with st.sidebar:
    st.markdown("### Crossfit med Malde")
    st.markdown("---")
    if st.session_state.is_trainer:
        st.markdown(f'**{st.session_state.display_name}** <span class="badge-trainer">Trener</span>', unsafe_allow_html=True)
    else:
        st.markdown(f"**{st.session_state.display_name}**")

    st.markdown("---")

    # Trainer PIN unlock
    if not st.session_state.is_trainer:
        with st.expander("Trener-tilgang"):
            pin_input = st.text_input("PIN-kode", type="password", key="pin_input")
            if st.button("Lås opp", key="btn_unlock"):
                if pin_input == TRAINER_PIN:
                    st.session_state.is_trainer = True
                    st.rerun()
                else:
                    st.error("Feil PIN")

    if st.button("Bytt bruker"):
        st.session_state.display_name = ""
        st.session_state.is_trainer = False
        st.rerun()

# ─── Load data ───────────────────────────────────────────────────────────────
df = load_signups()
wods = load_wods()

signed_up = is_signed_up(st.session_state.display_name, friday_str)
signups_today = df[df["date"] == friday_str] if not df.empty else pd.DataFrame()

# ─── SIGNUP CARD ─────────────────────────────────────────────────────────────
st.markdown(f'<div class="card"><h3>Fredag {friday_display}</h3>', unsafe_allow_html=True)

wod_info = wods.get(friday_str)
if wod_info:
    st.markdown('<span class="badge-orange">Dagens økt er klar</span>', unsafe_allow_html=True)
    st.markdown(f'<div class="wod-text">{wod_info["wod"]}</div>', unsafe_allow_html=True)
    st.markdown(f'<p style="color:#555;font-size:12px;margin-top:8px">Lagt inn av {wod_info.get("added_by","trener")}</p>', unsafe_allow_html=True)
else:
    st.markdown('*WOD ikke lagt inn ennå — kom tilbake snart!*')

st.markdown("<br>", unsafe_allow_html=True)

if signed_up:
    st.success("Du er påmeldt!")
    st.markdown('<div class="btn-secondary">', unsafe_allow_html=True)
    if st.button("Meld meg av"):
        remove_signup(st.session_state.display_name, friday_str)
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
else:
    if st.button("MELD MEG PÅ", key="btn_signup"):
        save_signup(st.session_state.display_name, friday_str)
        st.balloons()
        st.rerun()

st.markdown("</div>", unsafe_allow_html=True)

# ─── SIGNED UP LIST ──────────────────────────────────────────────────────────
if not signups_today.empty:
    st.markdown(f'<div class="card"><h3>Påmeldte ({len(signups_today)})</h3>', unsafe_allow_html=True)
    pills = "".join([f'<span class="signup-pill">{n}</span>' for n in signups_today["name"].tolist()])
    st.markdown(pills, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# ─── LEADERBOARD ─────────────────────────────────────────────────────────────
render_leaderboard(df, highlight_name=st.session_state.display_name)

# ═════════════════════════════════════════════════════════════════════════════
# TRAINER PANEL (unlocked via PIN)
# ═════════════════════════════════════════════════════════════════════════════
if st.session_state.is_trainer:
    st.markdown("---")
    st.markdown("## Trener-panel")

    # WOD editor
    st.markdown('<div class="card"><h3>Legg inn WOD</h3>', unsafe_allow_html=True)
    wod_date = st.date_input("Dato for økt", value=friday, key="wod_date")
    wod_text = st.text_area("Dagens WOD", height=180,
        placeholder="Eks:\n21-15-9\nThrusters 42.5/30 kg\nPull-ups\n\nFor tid",
        value=wods.get(str(wod_date), {}).get("wod", ""))
    if st.button("Lagre WOD", key="btn_save_wod"):
        if wod_text.strip():
            save_wod(str(wod_date), wod_text.strip(), st.session_state.display_name)
            st.success("WOD lagret!")
            st.rerun()
        else:
            st.error("Skriv inn WOD-tekst")
    st.markdown("</div>", unsafe_allow_html=True)

    # Manage signups
    st.markdown('<div class="card"><h3>Administrer påmeldinger</h3>', unsafe_allow_html=True)
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

    st.markdown("**Legg til deltaker manuelt**")
    manual_name = st.text_input("Navn", key="manual_name")
    if st.button("Legg til", key="btn_add_manual"):
        if manual_name.strip():
            if not is_signed_up(manual_name, str(manage_date)):
                save_signup(manual_name, str(manage_date))
                st.success(f"{manual_name} lagt til!")
                st.rerun()
            else:
                st.warning("Allerede påmeldt")
    st.markdown("</div>", unsafe_allow_html=True)
