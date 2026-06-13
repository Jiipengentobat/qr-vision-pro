import streamlit as st
from utils.database import init_db
from utils.auth import check_login, show_login_page

# ── Konfigurasi halaman ──────────────────────────────────────────────────────
st.set_page_config(
    page_title="QR Vision Pro",
    page_icon="🔳",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Inisialisasi database ────────────────────────────────────────────────────
init_db()

# ── Inject CSS global ────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=DM+Sans:wght@300;400;500;600&display=swap');

:root {
    --bg:       #0a0e1a;
    --surface:  #111827;
    --card:     #1a2235;
    --border:   #2a3a55;
    --accent:   #00e5ff;
    --accent2:  #7c3aed;
    --success:  #22c55e;
    --warning:  #f59e0b;
    --danger:   #ef4444;
    --text:     #e2e8f0;
    --muted:    #64748b;
}

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    background-color: var(--bg);
    color: var(--text);
}

/* Sidebar */
[data-testid="stSidebar"] {
    background: var(--surface);
    border-right: 1px solid var(--border);
}

/* Buttons */
.stButton > button {
    background: linear-gradient(135deg, var(--accent2), #4f46e5) !important;
    color: white !important;
    border: none !important;
    border-radius: 8px !important;
    font-family: 'DM Sans', sans-serif !important;
    font-weight: 600 !important;
    padding: 0.5rem 1.5rem !important;
    transition: all 0.2s ease !important;
}
.stButton > button:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 4px 20px rgba(124,58,237,0.4) !important;
}

/* Cards */
.qr-card {
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 1.5rem;
    margin-bottom: 1rem;
}

/* Metric boxes */
.metric-box {
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 1.2rem;
    text-align: center;
}
.metric-number {
    font-family: 'Space Mono', monospace;
    font-size: 2rem;
    font-weight: 700;
    color: var(--accent);
}
.metric-label {
    color: var(--muted);
    font-size: 0.85rem;
    margin-top: 4px;
}

/* Badge */
.badge {
    display: inline-block;
    padding: 2px 10px;
    border-radius: 99px;
    font-size: 0.75rem;
    font-weight: 600;
}
.badge-url    { background: rgba(0,229,255,0.15); color: var(--accent); }
.badge-text   { background: rgba(34,197,94,0.15);  color: var(--success); }
.badge-wifi   { background: rgba(245,158,11,0.15); color: var(--warning); }
.badge-other  { background: rgba(100,116,139,0.15);color: var(--muted); }

/* Hide default Streamlit header branding */
#MainMenu, footer, { visibility: hidden; }

/* Input fields */
.stTextInput > div > div > input,
.stTextArea > div > div > textarea {
    background: var(--card) !important;
    border: 1px solid var(--border) !important;
    color: var(--text) !important;
    border-radius: 8px !important;
}

/* Divider */
hr { border-color: var(--border); }
</style>
""", unsafe_allow_html=True)


# ── Auth gate ────────────────────────────────────────────────────────────────
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    show_login_page()
    st.stop()

# ── Sidebar navigasi ─────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='text-align:center; padding: 1rem 0 1.5rem'>
        <div style='font-family: Space Mono; font-size: 1.4rem; font-weight:700;
                    color: #00e5ff; letter-spacing: 2px;'>🔳 QR VISION</div>
        <div style='color: #64748b; font-size: 0.75rem; margin-top:4px;'>PRO EDITION</div>
    </div>
    """, unsafe_allow_html=True)

    menu = st.radio(
        "Navigasi",
        ["🏠  Beranda", "🔍  Scan QR", "✨  Generate QR", "📊  Dashboard", "🕘  Riwayat"],
        label_visibility="collapsed",
    )

    st.markdown("---")
    user = st.session_state.get("username", "User")
    st.markdown(f"<div style='color:#64748b; font-size:0.8rem;'>Login sebagai</div>"
                f"<div style='font-weight:600; color:#e2e8f0;'>👤 {user}</div>",
                unsafe_allow_html=True)
    if st.button("🚪 Logout", use_container_width=True):
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.rerun()

# ── Routing halaman ───────────────────────────────────────────────────────────
if   "Beranda"   in menu:
    from pages import home;      home.show()
elif "Scan QR"   in menu:
    from pages import scan;      scan.show()
elif "Generate"  in menu:
    from pages import generate;  generate.show()
elif "Dashboard" in menu:
    from pages import dashboard; dashboard.show()
elif "Riwayat"   in menu:
    from pages import history;   history.show()
