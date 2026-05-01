import sqlite3
from datetime import datetime
from config import Config

def get_db():
    # الاتصال بقاعدة البيانات مع خاصية التوقيت لمنع التعليق في السحاب
    return sqlite3.connect(Config.DB_PATH, check_same_thread=False, timeout=20)

def init_db():
    conn = get_db()
    c = conn.cursor()

    # جدول المستخدمين (الأدمن)
    c.execute("""
    CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT,
        role TEXT
    )
    """)

    # جدول التراخيص (المفاتيح المباعة)
    c.execute("""
    CREATE TABLE IF NOT EXISTS licenses(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        license_key TEXT UNIQUE,
        hwid TEXT,
        tier TEXT,
        status TEXT DEFAULT 'active',
        created_at TEXT
    )
    """)

    # جدول السجلات (لمراقبة العمليات)
    c.execute("""
    CREATE TABLE IF NOT EXISTS logs(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        event TEXT,
        created_at TEXT
    )
    """)

    conn.commit()
    conn.close()

def log_event(event):
    conn = get_db()
    c = conn.cursor()
    c.execute(
        "INSERT INTO logs(event, created_at) VALUES (?,?)",
        (event, datetime.utcnow().isoformat())
    )
    conn.commit()
    conn.close()
