# 🔳 QR Vision Pro
**Aplikasi Interaktif Deteksi & Generate QR Code Berbasis Web**  
DIF60202 – Image Processing | Semester Genap 2025/2026

---

## 📋 Deskripsi
QR Vision Pro adalah aplikasi web interaktif berbasis Python dan Streamlit yang memungkinkan pengguna untuk:
- **Scan QR Code** dari upload gambar atau kamera langsung
- **Generate QR Code** kustom (URL, WiFi, kontak, lokasi, dll.)
- **Melihat statistik** melalui dashboard analytics interaktif
- **Menyimpan riwayat** aktivitas dengan sistem login pengguna

---

## ✅ Fitur Lengkap
| Fitur | Status |
|-------|--------|
| Scan QR dari gambar (JPG/PNG/WEBP) | ✅ |
| Scan QR dari kamera/webcam | ✅ |
| Generate QR Code (6 tipe konten) | ✅ |
| Kustomisasi warna & style QR | ✅ |
| Download QR Code (PNG) | ✅ |
| Dashboard statistik (4 grafik) | ✅ |
| Riwayat scan & generate | ✅ |
| Sistem login & registrasi | ✅ |
| Database SQLite | ✅ |
| Klasifikasi tipe konten QR | ✅ |
| Confidence score & waktu inferensi | ✅ |

---

## 🛠️ Teknologi
- **Python 3.10+**
- **Streamlit** — Framework web
- **OpenCV** — Image processing & fallback decoder
- **pyzbar** — QR Code decoder (primary)
- **qrcode[pil]** — QR Code generator
- **Plotly** — Grafik interaktif
- **Pandas** — Manipulasi data
- **SQLite** — Database lokal

---

## 🚀 Cara Menjalankan (Lokal)

### 1. Clone / Extract project
```bash
cd qr_scanner_app
```

### 2. Install dependensi sistem (Linux/Ubuntu)
```bash
sudo apt-get install -y libzbar0
```
> Di Windows: install ZBar dari https://sourceforge.net/projects/zbar/

### 3. Install dependensi Python
```bash
pip install -r requirements.txt
```

### 4. Jalankan aplikasi
```bash
streamlit run app.py
```

### 5. Buka browser
```
http://localhost:8501
```

---

## 🔑 Akun Demo
```
Username : demo
Password : demo123
```

---

## ☁️ Cara Deploy ke Streamlit Cloud (GRATIS)

1. **Upload ke GitHub**
   - Buat repository baru di github.com
   - Upload seluruh isi folder `qr_scanner_app/`

2. **Daftar Streamlit Cloud**
   - Buka https://share.streamlit.io
   - Login dengan akun GitHub

3. **Deploy**
   - Klik "New app"
   - Pilih repository kamu
   - Main file path: `app.py`
   - Klik "Deploy!"

4. **Tambah packages.txt** (untuk libzbar)
   - Buat file `packages.txt` di root project:
     ```
     libzbar0
     ```

5. Aplikasi akan live di: `https://[nama-app].streamlit.app`

---

## 📁 Struktur Proyek
```
qr_scanner_app/
├── app.py                  ← Entry point utama
├── requirements.txt        ← Dependensi Python
├── packages.txt            ← Dependensi sistem (untuk deploy)
├── .streamlit/
│   └── config.toml         ← Konfigurasi tema dark
├── pages/
│   ├── home.py             ← Halaman Beranda
│   ├── scan.py             ← Halaman Scan QR
│   ├── generate.py         ← Halaman Generate QR
│   ├── dashboard.py        ← Dashboard Statistik
│   └── history.py          ← Riwayat Aktivitas
└── utils/
    ├── __init__.py
    ├── database.py         ← Operasi SQLite
    ├── auth.py             ← Autentikasi pengguna
    └── qr_processor.py     ← Core image processing
```

---

## 📊 Kriteria Penilaian yang Dipenuhi
| Komponen | Bobot | Status |
|----------|-------|--------|
| Implementasi Algoritma Image Processing | 25% | ✅ pyzbar + OpenCV + CLAHE |
| Fungsionalitas Sistem | 20% | ✅ Scan + Generate + Auth |
| UI/UX | 10% | ✅ Dark theme + Responsive |
| Inovasi dan Kreativitas | 10% | ✅ Multi-method + Dashboard |
| Demo video | 10% | 📹 Rekam sendiri |
| Poster | 10% | 🖼️ Template tersedia |
| Laporan | 10% | ✅ Laporan_QR_Vision_Pro.docx |
| Deployment Online | 5% | ☁️ Deploy ke Streamlit Cloud |

### Bonus (+10%) yang diupayakan:
- ✅ Dashboard Analytics lengkap
- ✅ Database + User Login
- ✅ Fitur di luar spesifikasi minimum (6 tipe generate, multi-method decoder)

---

## 📝 Pengumpulan Tugas
- **Email**: derisma@fti.unand.ac.id
- **Subjek**: `DIF60202_TugasBesar_NIM_Nama`
- **Deadline**: 16 Juni 2026, 23.59 WIB
