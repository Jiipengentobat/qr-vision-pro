"""
utils/auth.py
Halaman login & register untuk QR Vision Pro.
"""

import streamlit as st
from utils.database import verify_user, register_user


def check_login() -> bool:
    return st.session_state.get("logged_in", False)


def show_login_page():
    st.markdown("""
    <style>
    .login-wrap {
        max-width: 420px;
        margin: 6vh auto 0;
        background: #1a2235;
        border: 1px solid #2a3a55;
        border-radius: 16px;
        padding: 2.5rem 2rem;
    }
    .login-title {
        font-family: 'Space Mono', monospace;
        font-size: 1.8rem;
        font-weight: 700;
        color: #00e5ff;
        text-align: center;
        letter-spacing: 3px;
        margin-bottom: 4px;
    }
    .login-sub {
        text-align: center;
        color: #64748b;
        font-size: 0.85rem;
        margin-bottom: 1.8rem;
    }
    </style>

    <div class="login-wrap">
        <div class="login-title">🔳 QR VISION</div>
        <div class="login-sub">Image Processing — Semester Genap 2025/2026</div>
    </div>
    """, unsafe_allow_html=True)

    # Gunakan kolom tengah agar form muncul di tengah
    _, col, _ = st.columns([1, 2, 1])
    with col:
        tab_login, tab_reg = st.tabs(["🔐 Login", "📝 Daftar"])

        with tab_login:
            username = st.text_input("Username", key="li_user")
            password = st.text_input("Password", type="password", key="li_pass")
            if st.button("Masuk", use_container_width=True):
                if verify_user(username.strip(), password.strip()):
                    st.session_state.logged_in = True
                    st.session_state.username = username.strip()
                    st.rerun()
                else:
                    st.error("Username atau password salah.")
            st.caption("Demo: `demo` / `demo123`")

        with tab_reg:
            new_user = st.text_input("Username baru", key="reg_user")
            new_pass = st.text_input("Password baru", type="password", key="reg_pass")
            new_pass2 = st.text_input("Konfirmasi password", type="password", key="reg_pass2")
            if st.button("Daftar", use_container_width=True):
                if not new_user or not new_pass:
                    st.warning("Username dan password wajib diisi.")
                elif new_pass != new_pass2:
                    st.error("Password tidak cocok.")
                elif register_user(new_user.strip(), new_pass.strip()):
                    st.success("Akun berhasil dibuat! Silakan login.")
                else:
                    st.error("Username sudah digunakan.")
