import sqlite3
import random
import string
from datetime import datetime, timedelta

def connect():
    return sqlite3.connect("bot.db", check_same_thread=False)

def create_tables():
    conn = connect()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY,
        referral_code TEXT UNIQUE,
        invited_by INTEGER,
        points INTEGER DEFAULT 0
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS subscriptions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        months INTEGER,
        start TEXT,
        end TEXT,
        config TEXT
    )
    """)

    conn.commit()
    conn.close()

def generate_referral():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

def add_user(user_id, ref_code=None):
    conn = connect()
    cur = conn.cursor()

    cur.execute("SELECT * FROM users WHERE user_id=?", (user_id,))
    if cur.fetchone():
        conn.close()
        return

    my_code = generate_referral()

    invited_by = None
    if ref_code:
        cur.execute("SELECT user_id FROM users WHERE referral_code=?", (ref_code,))
        row = cur.fetchone()
        if row and row[0] != user_id:
            invited_by = row[0]

    cur.execute(
        "INSERT INTO users (user_id, referral_code, invited_by) VALUES (?, ?, ?)",
        (user_id, my_code, invited_by)
    )

    conn.commit()
    conn.close()

def get_user(user_id):
    conn = connect()
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE user_id=?", (user_id,))
    user = cur.fetchone()
    conn.close()
    return user

def add_points(user_id, amount):
    conn = connect()
    cur = conn.cursor()
    cur.execute("UPDATE users SET points = points + ? WHERE user_id=?", (amount, user_id))
    conn.commit()
    conn.close()

def create_subscription(user_id, months):
    conn = connect()
    cur = conn.cursor()

    start = datetime.now()
    end = start + timedelta(days=30*months)

    config = f"FAKE_WG_CONFIG_FOR_{user_id}"

    cur.execute("""
    INSERT INTO subscriptions (user_id, months, start, end, config)
    VALUES (?, ?, ?, ?, ?)
    """, (user_id, months, start.isoformat(), end.isoformat(), config))

    conn.commit()
    conn.close()

def get_subs(user_id):
    conn = connect()
    cur = conn.cursor()
    cur.execute("SELECT months, start, end, config FROM subscriptions WHERE user_id=?", (user_id,))
    subs = cur.fetchall()
    conn.close()
    return subs
