"""
pages/scan.py  –  Halaman Scan QR Code
"""
import streamlit as st
from PIL import Image
from utils.qr_processor import decode_qr
from utils.database import save_scan


def show():
    st.markdown("""
    <div style='padding: 1.5rem 0 0.5rem;'>
        <div style='font-family: Space Mono; font-size:0.8rem; color:#64748b;
                    letter-spacing:3px;'>IMAGE PROCESSING</div>
        <div style='font-size:1.8rem; font-weight:700; color:#e2e8f0; margin-top:4px;'>
            🔍 Scan QR Code
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    tab_upload, tab_cam = st.tabs(["📁 Upload Gambar", "📷 Webcam"])

    # ── Tab Upload ──────────────────────────────────────────────────────────
    with tab_upload:
        uploaded = st.file_uploader(
            "Pilih gambar berisi QR Code (JPG / PNG / WEBP)",
            type=["jpg", "jpeg", "png", "webp"],
            key="qr_upload",
        )

        if uploaded:
            image = Image.open(uploaded)
            col_img, col_result = st.columns([1, 1])

            with col_img:
                st.markdown("<div class='qr-card'>", unsafe_allow_html=True)
                st.markdown("**📷 Gambar Asli**")
                st.image(image, use_column_width=True)
                st.markdown(
                    f"<div style='color:#64748b; font-size:0.8rem;'>"
                    f"Ukuran: {image.width}×{image.height} px</div>",
                    unsafe_allow_html=True,
                )
                st.markdown("</div>", unsafe_allow_html=True)

            with col_result:
                with st.spinner("Memproses QR Code..."):
                    result = decode_qr(image)

                st.markdown("<div class='qr-card'>", unsafe_allow_html=True)
                st.markdown("**📊 Hasil Deteksi**")

                if result["success"]:
                    # Simpan ke DB
                    user = st.session_state.get("username", "guest")
                    save_scan(
                        user,
                        result["data"],
                        result["type"],
                        result["confidence"],
                        result["infer_ms"],
                    )

                    st.success("✅ QR Code berhasil terdeteksi!")

                    qr_type = result["type"]
                    badge_class = {
                        "URL": "badge-url",
                        "WiFi": "badge-wifi",
                        "Teks": "badge-text",
                    }.get(qr_type, "badge-other")

                    st.markdown(f"""
                    <div style='margin: 12px 0;'>
                        <span class="badge {badge_class}">{qr_type}</span>
                    </div>
                    """, unsafe_allow_html=True)

                    st.markdown("**Isi QR Code:**")
                    st.code(result["data"], language=None)

                    # Metrics
                    m1, m2, m3 = st.columns(3)
                    m1.metric("Confidence", f"{result['confidence']:.1f}%")
                    m2.metric("Waktu Inferensi", f"{result['infer_ms']:.1f} ms")
                    m3.metric("Metode", result["method"])

                    # Aksi cepat jika URL
                    if qr_type == "URL":
                        st.link_button("🌐 Buka URL", result["data"])

                else:
                    st.error("❌ Tidak ada QR Code yang terdeteksi.")
                    st.info(
                        "💡 Tips: Pastikan gambar jelas, tidak blur, dan QR Code "
                        "terlihat penuh dalam frame."
                    )
                    st.metric("Waktu Proses", f"{result['infer_ms']:.1f} ms")

                st.markdown("</div>", unsafe_allow_html=True)

    # ── Tab Webcam ──────────────────────────────────────────────────────────
    with tab_cam:
        st.markdown("""
        <div class="qr-card">
            <div style='font-family: Space Mono; color:#00e5ff; font-size:0.8rem;
                        letter-spacing:2px; margin-bottom:12px;'>📷 KAMERA LANGSUNG</div>
            <p style='color:#cbd5e1;'>
                Gunakan kamera perangkat untuk scan QR Code secara langsung.
                Klik <b>Take Photo</b> setelah mengarahkan kamera ke QR Code.
            </p>
        </div>
        """, unsafe_allow_html=True)

        cam_img = st.camera_input("Arahkan kamera ke QR Code")

        if cam_img:
            image = Image.open(cam_img)
            col_img, col_result = st.columns([1, 1])

            with col_img:
                st.markdown("**📷 Foto dari Kamera**")
                st.image(image, use_column_width=True)

            with col_result:
                with st.spinner("Memproses..."):
                    result = decode_qr(image)

                if result["success"]:
                    user = st.session_state.get("username", "guest")
                    save_scan(
                        user,
                        result["data"],
                        result["type"],
                        result["confidence"],
                        result["infer_ms"],
                    )

                    st.success("✅ QR Code berhasil terdeteksi!")
                    st.markdown(f"**Tipe:** `{result['type']}`")
                    st.code(result["data"], language=None)
                    c1, c2 = st.columns(2)
                    c1.metric("Confidence", f"{result['confidence']:.1f}%")
                    c2.metric("Inferensi", f"{result['infer_ms']:.1f} ms")
                    if result["type"] == "URL":
                        st.link_button("🌐 Buka URL", result["data"])
                else:
                    st.error("❌ QR Code tidak terdeteksi. Coba ambil foto ulang.")
                    st.metric("Waktu Proses", f"{result['infer_ms']:.1f} ms")
