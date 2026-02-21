import streamlit as st
import pandas as pd
import os
from datetime import datetime, date
import json

# ─── PAGE CONFIG ────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Friday WOD 🏋️",
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
    content: "WOD";
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
</style>
""", unsafe_allow_html=True)

# ─── DATA HELPERS ────────────────────────────────────────────────────────────
SIGNUPS_FILE = "signups.csv"
WOD_FILE     = "wods.json"

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

def save_wod(session_date: str, wod_text: str, admin_name: str):
    wods = load_wods()
    wods[session_date] = {"wod": wod_text, "added_by": admin_name, "updated": datetime.now().isoformat()}
    with open(WOD_FILE, "w") as f:
        json.dump(wods, f, indent=2)

# ─── NEXT FRIDAY ─────────────────────────────────────────────────────────────
def next_friday() -> date:
    today = date.today()
    days_ahead = 4 - today.weekday()  # Friday is weekday 4
    if days_ahead < 0:
        days_ahead += 7
    elif days_ahead == 0:
        pass
    return today + __import__("datetime").timedelta(days=days_ahead)

# ─── SESSION STATE ───────────────────────────────────────────────────────────
if "user_name" not in st.session_state:
    st.session_state.user_name = ""
if "is_admin" not in st.session_state:
    st.session_state.is_admin = False

ADMIN_PASSWORD = "crossfit2025"  # ← Endre dette til noe bedre!

# ─── SIDEBAR: LOGIN ──────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🏋️ Friday WOD")
    st.markdown("---")

    if not st.session_state.user_name:
        st.markdown("### Hvem er du?")
        name_input = st.text_input("Ditt navn", placeholder="Ola Nordmann")
        if st.button("Logg inn"):
            if name_input.strip():
                st.session_state.user_name = name_input.strip()
                st.rerun()
            else:
                st.error("Skriv inn navnet ditt!")
    else:
        st.markdown(f"**Logget inn som:**")
        st.markdown(f"### {st.session_state.user_name}")
        if st.button("Bytt bruker"):
            st.session_state.user_name = ""
            st.session_state.is_admin = False
            st.rerun()

    st.markdown("---")
    st.markdown("### 🔐 Admin")
    if not st.session_state.is_admin:
        pwd = st.text_input("Admin-passord", type="password")
        if st.button("Admin-tilgang"):
            if pwd == ADMIN_PASSWORD:
                st.session_state.is_admin = True
                st.success("Admin aktivert!")
                st.rerun()
            elif pwd:
                st.error("Feil passord")
    else:
        st.success("✅ Admin-modus")
        if st.button("Avslutt admin"):
            st.session_state.is_admin = False
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
    <h1>Friday WOD 🔥</h1>
    <p>Neste økt: Fredag {friday_display}</p>
</div>
""", unsafe_allow_html=True)

# ─── GATE: Ikke logget inn ───────────────────────────────────────────────────
if not st.session_state.user_name:
    st.info("👈 Skriv inn navnet ditt i sidepanelet for å komme i gang!")
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

signed_up   = is_signed_up(st.session_state.user_name, friday_str)
signups_today = df[df["date"] == friday_str] if not df.empty else pd.DataFrame()
total_sessions = len(df[df["name"].str.lower() == st.session_state.user_name.lower()]) if not df.empty else 0

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
        st.markdown(f'<p style="color:#555;font-size:12px;margin-top:8px">Lagt inn av {wod_info.get("added_by","admin")}</p>', unsafe_allow_html=True)
    else:
        st.markdown('*WOD ikke lagt inn ennå – kom tilbake snart!*')

    st.markdown("<br>", unsafe_allow_html=True)

    if signed_up:
        st.success(f"✅ Du er påmeldt!")
        if st.button("Meld meg av"):
            remove_signup(st.session_state.user_name, friday_str)
            st.rerun()
    else:
        if st.button("🔥 MELD MEG PÅ"):
            save_signup(st.session_state.user_name, friday_str)
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
            you   = " 👈" if row["name"].lower() == st.session_state.user_name.lower() else ""
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

# ─── ADMIN PANEL ─────────────────────────────────────────────────────────────
if st.session_state.is_admin:
    st.markdown("---")
    st.markdown("## 🔐 Admin-panel")
    a1, a2 = st.columns(2)

    with a1:
        st.markdown('<div class="card"><h3>📝 Legg inn WOD</h3>', unsafe_allow_html=True)
        wod_date = st.date_input("Dato for økt", value=friday, key="wod_date")
        wod_text = st.text_area("Dagens WOD", height=180,
            placeholder="Eks:\n21-15-9\nThrusters 42.5/30 kg\nPull-ups\n\nFor tid ⏱️",
            value=wods.get(str(wod_date), {}).get("wod", ""))
        if st.button("💾 Lagre WOD"):
            if wod_text.strip():
                save_wod(str(wod_date), wod_text.strip(), st.session_state.user_name)
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
