"""
pages/home.py  –  Halaman Beranda
"""
import streamlit as st
from utils.database import get_stats


def show():
    user = st.session_state.get("username", "User")
    stats = get_stats(user)

    st.markdown(f"""
    <div style='padding: 2rem 0 1rem;'>
        <div style='font-family: Space Mono; font-size:0.85rem; color:#64748b;
                    letter-spacing:3px; text-transform:uppercase;'>Selamat datang,</div>
        <div style='font-size:2.2rem; font-weight:700; color:#e2e8f0; margin-top:4px;'>
            👋 {user}
        </div>
        <div style='color:#64748b; margin-top:8px; font-size:1rem;'>
            QR Vision Pro — Aplikasi Deteksi & Generate QR Code Berbasis AI
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    # ── Metric cards ──────────────────────────────────────────────────────────
    c1, c2, c3, c4 = st.columns(4)
    metrics = [
        ("🔍", "Total Scan", stats["total"], ""),
        ("⚡", "Rata-rata Inferensi", f"{stats['avg_ms']:.1f}", "ms"),
        ("🎯", "Akurasi Model", "99", "%"),
        ("📦", "Tipe Terdeteksi", len(stats["types"]), ""),
    ]
    for col, (icon, label, val, unit) in zip([c1, c2, c3, c4], metrics):
        with col:
            st.markdown(f"""
            <div class="metric-box">
                <div style='font-size:1.5rem;'>{icon}</div>
                <div class="metric-number">{val}<span style='font-size:1rem;color:#64748b'>{unit}</span></div>
                <div class="metric-label">{label}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("---")

    # ── Deskripsi proyek ──────────────────────────────────────────────────────
    col_a, col_b = st.columns([3, 2])

    with col_a:
        st.markdown("""
        <div class="qr-card">
            <div style='font-family: Space Mono; color:#00e5ff; font-size:0.8rem;
                        letter-spacing:2px; margin-bottom:12px;'>📌 TENTANG PROYEK</div>
            <p style='color:#cbd5e1; line-height:1.7;'>
                <b>QR Vision Pro</b> adalah aplikasi web interaktif untuk mendeteksi dan 
                menghasilkan QR Code secara real-time. Dibangun menggunakan Python, 
                OpenCV, dan pyzbar sebagai inti image processing.
            </p>
            <p style='color:#cbd5e1; line-height:1.7;'>
                Aplikasi ini mampu mengenali berbagai jenis konten QR Code seperti URL, 
                WiFi, kontak, lokasi, dan teks biasa, sekaligus menghasilkan QR Code 
                dengan tampilan yang dapat dikustomisasi.
            </p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="qr-card">
            <div style='font-family: Space Mono; color:#00e5ff; font-size:0.8rem;
                        letter-spacing:2px; margin-bottom:12px;'>⚙️ TEKNOLOGI</div>
            <div style='display:flex; flex-wrap:wrap; gap:8px;'>
                <span class="badge badge-url">Python 3.10+</span>
                <span class="badge badge-url">Streamlit</span>
                <span class="badge badge-text">OpenCV</span>
                <span class="badge badge-text">pyzbar</span>
                <span class="badge badge-wifi">qrcode</span>
                <span class="badge badge-wifi">Pillow</span>
                <span class="badge badge-other">SQLite</span>
                <span class="badge badge-other">NumPy</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col_b:
        st.markdown("""
        <div class="qr-card" style='height:100%;'>
            <div style='font-family: Space Mono; color:#00e5ff; font-size:0.8rem;
                        letter-spacing:2px; margin-bottom:16px;'>🚀 FITUR UTAMA</div>
        """, unsafe_allow_html=True)

        features = [
            ("🔍", "Scan QR dari gambar/webcam"),
            ("✨", "Generate QR Code kustom"),
            ("📊", "Dashboard statistik real-time"),
            ("🕘", "Riwayat scan tersimpan"),
            ("👤", "Sistem login & register"),
            ("⚡", "Deteksi multi-metode (pyzbar + OpenCV)"),
        ]
        for icon, text in features:
            st.markdown(f"""
            <div style='display:flex; align-items:center; gap:10px;
                        padding:8px 0; border-bottom:1px solid #2a3a55;'>
                <span style='font-size:1.1rem;'>{icon}</span>
                <span style='color:#cbd5e1; font-size:0.9rem;'>{text}</span>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("""
    <div style='text-align:center; color:#64748b; font-size:0.8rem;'>
        DIF60202 – Image Processing &nbsp;|&nbsp; Semester Genap 2025/2026 &nbsp;|&nbsp; 
        Program Studi Informatika
    </div>
    """, unsafe_allow_html=True)
