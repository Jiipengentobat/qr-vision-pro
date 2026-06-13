"""
utils/qr_processor.py
Fungsi decode & encode QR Code + deteksi tipe konten.
Windows-compatible: pyzbar opsional, fallback ke OpenCV + opencv-python.
"""

import time
import io
import re
import numpy as np
from PIL import Image
import cv2
import qrcode
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.moduledrawers.pil import RoundedModuleDrawer

# pyzbar opsional — kalau DLL tidak ada di Windows, skip saja
try:
    from pyzbar.pyzbar import decode as pyzbar_decode
    PYZBAR_OK = True
except Exception:
    PYZBAR_OK = False


# ── Decode ────────────────────────────────────────────────────────────────────
def decode_qr(image: Image.Image) -> dict:
    t0 = time.perf_counter()

    img_array = np.array(image.convert("RGB"))
    img_bgr   = cv2.cvtColor(img_array, cv2.COLOR_RGB2BGR)
    img_gray  = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)

    # ── Metode 1: pyzbar (kalau tersedia) ────────────────────────────────────
    if PYZBAR_OK:
        decoded = pyzbar_decode(image)
        if not decoded:
            clahe        = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
            enhanced     = clahe.apply(img_gray)
            enhanced_pil = Image.fromarray(enhanced)
            decoded      = pyzbar_decode(enhanced_pil)

        if decoded:
            data    = decoded[0].data.decode("utf-8", errors="replace")
            elapsed = (time.perf_counter() - t0) * 1000
            return {
                "success": True, "data": data,
                "type": classify_qr_content(data),
                "confidence": 99.0, "infer_ms": round(elapsed, 2),
                "method": "pyzbar",
            }

    # ── Metode 2: OpenCV QRCodeDetector ──────────────────────────────────────
    detector = cv2.QRCodeDetector()

    # Coba gambar asli
    data, points, _ = detector.detectAndDecode(img_bgr)
    if not data:
        # Pre-process: CLAHE
        clahe    = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        enhanced = clahe.apply(img_gray)
        data, points, _ = detector.detectAndDecode(enhanced)
    if not data:
        # Pre-process: threshold
        _, thresh = cv2.threshold(img_gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        data, points, _ = detector.detectAndDecode(thresh)
    if not data:
        # Pre-process: upscale kecil
        big  = cv2.resize(img_bgr, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
        data, points, _ = detector.detectAndDecode(big)

    elapsed = (time.perf_counter() - t0) * 1000
    if data:
        return {
            "success": True, "data": data,
            "type": classify_qr_content(data),
            "confidence": 92.0, "infer_ms": round(elapsed, 2),
            "method": "OpenCV",
        }

    # ── Metode 3: opencv-contrib WeChatQRCode (kalau ada) ────────────────────
    try:
        wechat = cv2.wechat_qrcode_WeChatQRCode()
        texts, _ = wechat.detectAndDecode(img_bgr)
        if texts and texts[0]:
            data    = texts[0]
            elapsed = (time.perf_counter() - t0) * 1000
            return {
                "success": True, "data": data,
                "type": classify_qr_content(data),
                "confidence": 95.0, "infer_ms": round(elapsed, 2),
                "method": "WeChatQR",
            }
    except Exception:
        pass

    return {
        "success": False, "data": None, "type": None,
        "confidence": 0.0, "infer_ms": round(elapsed, 2), "method": None,
    }


def classify_qr_content(data: str) -> str:
    d = data.strip()
    if re.match(r"^https?://", d, re.I):      return "URL"
    if re.match(r"^WIFI:", d, re.I):           return "WiFi"
    if re.match(r"^(BEGIN:VCARD|BEGIN:VEVENT)", d, re.I): return "vCard/vCal"
    if re.match(r"^(mailto:|tel:|smsto:|sms:)", d, re.I): return "Kontak"
    if re.match(r"^geo:", d, re.I):            return "Lokasi"
    if d.isdigit():                            return "Numerik"
    return "Teks"


# ── Encode ────────────────────────────────────────────────────────────────────
def generate_qr(
    data: str,
    fg_color: str = "#00e5ff",
    bg_color: str = "#0a0e1a",
    box_size: int = 10,
    border: int = 2,
    rounded: bool = True,
) -> Image.Image:
    qr = qrcode.QRCode(
        version=None,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=box_size,
        border=border,
    )
    qr.add_data(data)
    qr.make(fit=True)

    if rounded:
        img = qr.make_image(
            image_factory=StyledPilImage,
            module_drawer=RoundedModuleDrawer(),
            fill_color=fg_color,
            back_color=bg_color,
        )
    else:
        img = qr.make_image(fill_color=fg_color, back_color=bg_color)

    return img.convert("RGBA")


def pil_to_bytes(img: Image.Image, fmt: str = "PNG") -> bytes:
    buf = io.BytesIO()
    img.save(buf, format=fmt)
    return buf.getvalue()
