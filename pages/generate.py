"""
pages/generate.py  –  Halaman Generate QR Code
"""
import streamlit as st
from utils.qr_processor import generate_qr, pil_to_bytes
from utils.database import save_generated


def show():
    st.markdown("""
    <div style='padding: 1.5rem 0 0.5rem;'>
        <div style='font-family: Space Mono; font-size:0.8rem; color:#64748b;
                    letter-spacing:3px;'>IMAGE PROCESSING</div>
        <div style='font-size:1.8rem; font-weight:700; color:#e2e8f0; margin-top:4px;'>
            ✨ Generate QR Code
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("---")

    col_form, col_preview = st.columns([1, 1])

    with col_form:
        st.markdown("<div class='qr-card'>", unsafe_allow_html=True)
        st.markdown("**⚙️ Konfigurasi QR Code**")

        qr_type = st.selectbox(
            "Tipe Konten",
            ["URL / Link", "Teks Biasa", "WiFi", "Nomor Telepon", "Email", "Lokasi GPS"],
        )

        # Input dinamis berdasarkan tipe
        data = ""
        if qr_type == "URL / Link":
            url = st.text_input("Masukkan URL", placeholder="https://example.com")
            data = url

        elif qr_type == "Teks Biasa":
            data = st.text_area("Masukkan teks", placeholder="Tulis apapun di sini...")

        elif qr_type == "WiFi":
            ssid = st.text_input("Nama WiFi (SSID)")
            pwd  = st.text_input("Password WiFi", type="password")
            enc  = st.selectbox("Enkripsi", ["WPA", "WEP", "nopass"])
            data = f"WIFI:T:{enc};S:{ssid};P:{pwd};;"

        elif qr_type == "Nomor Telepon":
            phone = st.text_input("Nomor telepon", placeholder="+62812345678")
            data = f"tel:{phone}"

        elif qr_type == "Email":
            email   = st.text_input("Alamat email")
            subject = st.text_input("Subjek (opsional)")
            body    = st.text_area("Isi pesan (opsional)")
            data = f"mailto:{email}?subject={subject}&body={body}"

        elif qr_type == "Lokasi GPS":
            lat = st.number_input("Latitude",  value=-0.9471, format="%.6f")
            lon = st.number_input("Longitude", value=100.4172, format="%.6f")
            data = f"geo:{lat},{lon}"

        st.markdown("---")
        st.markdown("**🎨 Kustomisasi Tampilan**")

        c1, c2 = st.columns(2)
        fg_color = c1.color_picker("Warna QR", "#00e5ff")
        bg_color = c2.color_picker("Warna latar", "#0a0e1a")
        rounded  = st.toggle("Modul membulat", value=True)

        generate_btn = st.button("🚀 Generate QR Code", use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with col_preview:
        st.markdown("<div class='qr-card' style='text-align:center;'>",
                    unsafe_allow_html=True)
        st.markdown("**👁️ Preview**")

        if generate_btn and data.strip():
            with st.spinner("Membuat QR Code..."):
                img = generate_qr(
                    data.strip(),
                    fg_color=fg_color,
                    bg_color=bg_color,
                    rounded=rounded,
                )
            st.image(img, width=300, caption="QR Code kamu")

            img_bytes = pil_to_bytes(img)
            st.download_button(
                "⬇️ Download QR Code (PNG)",
                data=img_bytes,
                file_name="qrcode.png",
                mime="image/png",
                use_container_width=True,
            )

            # Simpan ke riwayat
            user = st.session_state.get("username", "guest")
            save_generated(user, data.strip(), qr_type)
            st.success("✅ QR Code berhasil dibuat dan disimpan ke riwayat!")

        elif generate_btn and not data.strip():
            st.warning("⚠️ Isi data QR Code terlebih dahulu.")
        else:
            st.markdown("""
            <div style='padding:4rem 0; color:#64748b; font-size:0.9rem;'>
                <div style='font-size:3rem;'>🔳</div>
                <div style='margin-top:12px;'>QR Code akan muncul di sini</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)
