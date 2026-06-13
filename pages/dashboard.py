"""
pages/dashboard.py  –  Halaman Dashboard Statistik
"""
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from utils.database import get_all_scan_history, get_stats


PLOTLY_THEME = {
    "paper_bgcolor": "rgba(0,0,0,0)",
    "plot_bgcolor":  "rgba(0,0,0,0)",
    "font":          {"color": "#e2e8f0", "family": "DM Sans"},
    "xaxis":         {"gridcolor": "#2a3a55", "zerolinecolor": "#2a3a55"},
    "yaxis":         {"gridcolor": "#2a3a55", "zerolinecolor": "#2a3a55"},
}


def apply_theme(fig):
    fig.update_layout(**PLOTLY_THEME)
    return fig


def show():
    st.markdown("""
    <div style='padding: 1.5rem 0 0.5rem;'>
        <div style='font-family: Space Mono; font-size:0.8rem; color:#64748b;
                    letter-spacing:3px;'>ANALYTICS</div>
        <div style='font-size:1.8rem; font-weight:700; color:#e2e8f0; margin-top:4px;'>
            📊 Dashboard Statistik
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("---")

    user  = st.session_state.get("username", "guest")
    stats = get_stats(user)
    rows  = get_all_scan_history(limit=500)

    if not rows:
        st.info("📭 Belum ada data scan. Coba scan QR Code dulu di halaman Scan QR.")
        return

    df = pd.DataFrame(rows)
    df["scanned_at"] = pd.to_datetime(df["scanned_at"])
    df["date"]       = df["scanned_at"].dt.date

    # ── Metric row ────────────────────────────────────────────────────────────
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(f"""<div class="metric-box">
            <div style='font-size:1.5rem;'>🔍</div>
            <div class="metric-number">{stats['total']}</div>
            <div class="metric-label">Total Scan</div>
        </div>""", unsafe_allow_html=True)
    with c2:
        st.markdown(f"""<div class="metric-box">
            <div style='font-size:1.5rem;'>⚡</div>
            <div class="metric-number">{stats['avg_ms']:.1f}<span style='font-size:0.9rem;color:#64748b'>ms</span></div>
            <div class="metric-label">Rata-rata Inferensi</div>
        </div>""", unsafe_allow_html=True)
    with c3:
        avg_conf = df["confidence"].mean() if "confidence" in df.columns else 99
        st.markdown(f"""<div class="metric-box">
            <div style='font-size:1.5rem;'>🎯</div>
            <div class="metric-number">{avg_conf:.1f}<span style='font-size:0.9rem;color:#64748b'>%</span></div>
            <div class="metric-label">Rata-rata Confidence</div>
        </div>""", unsafe_allow_html=True)
    with c4:
        n_types = len(stats["types"])
        st.markdown(f"""<div class="metric-box">
            <div style='font-size:1.5rem;'>📦</div>
            <div class="metric-number">{n_types}</div>
            <div class="metric-label">Jenis QR Terdeteksi</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("---")

    # ── Charts row 1 ─────────────────────────────────────────────────────────
    col_pie, col_bar = st.columns(2)

    with col_pie:
        type_counts = df["qr_type"].value_counts().reset_index()
        type_counts.columns = ["Tipe", "Jumlah"]
        fig_pie = px.pie(
            type_counts, names="Tipe", values="Jumlah",
            title="Distribusi Tipe QR Code",
            color_discrete_sequence=["#00e5ff", "#7c3aed", "#22c55e", "#f59e0b", "#ef4444"],
            hole=0.4,
        )
        apply_theme(fig_pie)
        fig_pie.update_traces(textfont_color="white")
        st.plotly_chart(fig_pie, use_container_width=True)

    with col_bar:
        daily = df.groupby("date").size().reset_index(name="Jumlah Scan")
        fig_bar = px.bar(
            daily, x="date", y="Jumlah Scan",
            title="Aktivitas Scan Harian",
            color_discrete_sequence=["#7c3aed"],
        )
        apply_theme(fig_bar)
        st.plotly_chart(fig_bar, use_container_width=True)

    # ── Charts row 2 ─────────────────────────────────────────────────────────
    col_infer, col_conf = st.columns(2)

    with col_infer:
        fig_infer = px.histogram(
            df, x="infer_ms", nbins=20,
            title="Distribusi Waktu Inferensi (ms)",
            color_discrete_sequence=["#00e5ff"],
        )
        apply_theme(fig_infer)
        st.plotly_chart(fig_infer, use_container_width=True)

    with col_conf:
        fig_conf = px.box(
            df, x="qr_type", y="confidence",
            title="Confidence Score per Tipe QR",
            color="qr_type",
            color_discrete_sequence=["#00e5ff","#7c3aed","#22c55e","#f59e0b","#ef4444"],
        )
        apply_theme(fig_conf)
        st.plotly_chart(fig_conf, use_container_width=True)

    st.markdown("---")

    # ── Data table ────────────────────────────────────────────────────────────
    st.markdown("**📋 Data Scan Terbaru**")
    display_df = df[["username", "qr_type", "confidence", "infer_ms", "scanned_at"]].copy()
    display_df.columns = ["User", "Tipe QR", "Confidence (%)", "Inferensi (ms)", "Waktu Scan"]
    st.dataframe(display_df.head(20), use_container_width=True, hide_index=True)
