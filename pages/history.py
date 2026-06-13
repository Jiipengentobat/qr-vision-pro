"""
pages/history.py  –  Halaman Riwayat Scan & Generate
"""
import streamlit as st
import pandas as pd
from utils.database import get_scan_history, get_generated_history


def show():
    st.markdown("""
    <div style='padding: 1.5rem 0 0.5rem;'>
        <div style='font-family: Space Mono; font-size:0.8rem; color:#64748b;
                    letter-spacing:3px;'>RIWAYAT AKTIVITAS</div>
        <div style='font-size:1.8rem; font-weight:700; color:#e2e8f0; margin-top:4px;'>
            🕘 Riwayat
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("---")

    user = st.session_state.get("username", "guest")

    tab_scan, tab_gen = st.tabs(["🔍 Scan QR", "✨ Generate QR"])

    # ── Riwayat Scan ──────────────────────────────────────────────────────────
    with tab_scan:
        scans = get_scan_history(user, limit=100)
        if not scans:
            st.info("📭 Belum ada riwayat scan.")
        else:
            df = pd.DataFrame(scans)
            df = df[["qr_type", "qr_data", "confidence", "infer_ms", "scanned_at"]]
            df.columns = ["Tipe", "Isi QR", "Confidence (%)", "Inferensi (ms)", "Waktu"]

            # Filter tipe
            all_types = ["Semua"] + sorted(df["Tipe"].unique().tolist())
            sel = st.selectbox("Filter Tipe QR", all_types)
            if sel != "Semua":
                df = df[df["Tipe"] == sel]

            st.markdown(f"<div style='color:#64748b; margin-bottom:8px;'>"
                        f"Menampilkan {len(df)} entri</div>", unsafe_allow_html=True)

            for _, row in df.iterrows():
                badge_class = {
                    "URL": "badge-url",
                    "WiFi": "badge-wifi",
                    "Teks": "badge-text",
                }.get(row["Tipe"], "badge-other")

                with st.expander(f"🔍 {row['Tipe']}  —  {str(row['Isi QR'])[:60]}..."):
                    st.markdown(f"""
                    <div class="qr-card">
                        <span class="badge {badge_class}">{row['Tipe']}</span>
                        <div style='margin: 10px 0; color:#cbd5e1; word-break:break-all;'>
                            {row['Isi QR']}
                        </div>
                        <div style='display:flex; gap:2rem; color:#64748b; font-size:0.85rem;'>
                            <span>⚡ {row['Inferensi (ms)']} ms</span>
                            <span>🎯 {row['Confidence (%)']}%</span>
                            <span>🕐 {row['Waktu']}</span>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    if row["Tipe"] == "URL":
                        st.link_button("🌐 Buka URL", row["Isi QR"])

    # ── Riwayat Generate ─────────────────────────────────────────────────────
    with tab_gen:
        gens = get_generated_history(user, limit=50)
        if not gens:
            st.info("📭 Belum ada riwayat generate QR.")
        else:
            for item in gens:
                with st.expander(f"✨ {item['qr_type']}  —  {str(item['content'])[:60]}"):
                    st.markdown(f"""
                    <div class="qr-card">
                        <div style='color:#cbd5e1; word-break:break-all; margin-bottom:8px;'>
                            {item['content']}
                        </div>
                        <div style='color:#64748b; font-size:0.85rem;'>
                            📦 Tipe: {item['qr_type']} &nbsp;|&nbsp; 🕐 {item['created_at']}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
