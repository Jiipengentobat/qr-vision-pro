"""
utils/database.py
Semua operasi SQLite untuk QR Vision Pro.
"""

import sqlite3
import os
from datetime import datetime

DB_PATH = "qr_vision.db"


def get_conn():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Buat tabel jika belum ada."""
    conn = get_conn()
    c = conn.cursor()

    # Tabel users
    c.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id       INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT    UNIQUE NOT NULL,
            password TEXT    NOT NULL,
            created  TEXT    DEFAULT (datetime('now','localtime'))
        )
    """)

    # Tabel scan history
    c.execute("""
        CREATE TABLE IF NOT EXISTS scan_history (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            username    TEXT    NOT NULL,
            qr_data     TEXT    NOT NULL,
            qr_type     TEXT    DEFAULT 'unknown',
            confidence  REAL    DEFAULT 100.0,
            infer_ms    REAL    DEFAULT 0.0,
            scanned_at  TEXT    DEFAULT (datetime('now','localtime'))
        )
    """)

    # Tabel generated QR
    c.execute("""
        CREATE TABLE IF NOT EXISTS generated_qr (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            username    TEXT NOT NULL,
            content     TEXT NOT NULL,
            qr_type     TEXT DEFAULT 'custom',
            created_at  TEXT DEFAULT (datetime('now','localtime'))
        )
    """)

    # Seed user demo jika tabel kosong
    c.execute("SELECT COUNT(*) FROM users")
    if c.fetchone()[0] == 0:
        c.execute(
            "INSERT INTO users (username, password) VALUES (?, ?)",
            ("demo", "demo123"),
        )

    conn.commit()
    conn.close()


# ── User auth ────────────────────────────────────────────────────────────────
def user_exists(username: str) -> bool:
    conn = get_conn()
    row = conn.execute("SELECT id FROM users WHERE username=?", (username,)).fetchone()
    conn.close()
    return row is not None


def verify_user(username: str, password: str) -> bool:
    conn = get_conn()
    row = conn.execute(
        "SELECT id FROM users WHERE username=? AND password=?", (username, password)
    ).fetchone()
    conn.close()
    return row is not None


def register_user(username: str, password: str) -> bool:
    if user_exists(username):
        return False
    conn = get_conn()
    conn.execute("INSERT INTO users (username, password) VALUES (?,?)", (username, password))
    conn.commit()
    conn.close()
    return True


# ── Scan history ─────────────────────────────────────────────────────────────
def save_scan(username, qr_data, qr_type, confidence, infer_ms):
    conn = get_conn()
    conn.execute(
        "INSERT INTO scan_history (username,qr_data,qr_type,confidence,infer_ms) VALUES (?,?,?,?,?)",
        (username, qr_data, qr_type, confidence, infer_ms),
    )
    conn.commit()
    conn.close()


def get_scan_history(username: str, limit: int = 50):
    conn = get_conn()
    rows = conn.execute(
        "SELECT * FROM scan_history WHERE username=? ORDER BY id DESC LIMIT ?",
        (username, limit),
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_all_scan_history(limit: int = 200):
    conn = get_conn()
    rows = conn.execute(
        "SELECT * FROM scan_history ORDER BY id DESC LIMIT ?", (limit,)
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]


# ── Stats ────────────────────────────────────────────────────────────────────
def get_stats(username: str):
    conn = get_conn()
    total = conn.execute(
        "SELECT COUNT(*) FROM scan_history WHERE username=?", (username,)
    ).fetchone()[0]
    avg_ms = conn.execute(
        "SELECT AVG(infer_ms) FROM scan_history WHERE username=?", (username,)
    ).fetchone()[0] or 0
    types = conn.execute(
        "SELECT qr_type, COUNT(*) as cnt FROM scan_history WHERE username=? GROUP BY qr_type",
        (username,),
    ).fetchall()
    conn.close()
    return {
        "total": total,
        "avg_ms": round(avg_ms, 2),
        "types": {r["qr_type"]: r["cnt"] for r in types},
    }


# ── Generated QR ─────────────────────────────────────────────────────────────
def save_generated(username, content, qr_type="custom"):
    conn = get_conn()
    conn.execute(
        "INSERT INTO generated_qr (username,content,qr_type) VALUES (?,?,?)",
        (username, content, qr_type),
    )
    conn.commit()
    conn.close()


def get_generated_history(username: str, limit: int = 30):
    conn = get_conn()
    rows = conn.execute(
        "SELECT * FROM generated_qr WHERE username=? ORDER BY id DESC LIMIT ?",
        (username, limit),
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]
