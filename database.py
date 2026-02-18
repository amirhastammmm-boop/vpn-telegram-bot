import sqlite3
from datetime import datetime, timedelta

DB_NAME = "bot.db"


def connect():
    return sqlite3.connect(DB_NAME)


# =========================
# ساخت جدول ها
# =========================

def create_tables():

    conn = connect()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS subscriptions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        buy_date TEXT,
        expire_date TEXT,
        volume TEXT
    )
    """)

    conn.commit()
    conn.close()


def create_users_table():

    conn = connect()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY,
        referral TEXT,
        points INTEGER DEFAULT 0
    )
    """)

    conn.commit()
    conn.close()


# =========================
# USER
# =========================

def add_user(user_id, referral=None):

    conn = connect()
    cur = conn.cursor()

    cur.execute(
        "INSERT OR IGNORE INTO users (user_id, referral) VALUES (?, ?)",
        (user_id, referral)
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

    cur.execute(
        "UPDATE users SET points = points + ? WHERE user_id=?",
        (amount, user_id)
    )

    conn.commit()
    conn.close()


def get_user_points(user_id):

    conn = connect()
    cur = conn.cursor()

    cur.execute("SELECT points FROM users WHERE user_id=?", (user_id,))
    row = cur.fetchone()

    conn.close()

    return row[0] if row else 0


# =========================
# SUBSCRIPTIONS
# =========================

def add_subscription(user_id, days, volume):

    conn = connect()
    cur = conn.cursor()

    buy_date = datetime.now()
    expire_date = buy_date + timedelta(days=days)

    cur.execute("""
        INSERT INTO subscriptions (user_id, buy_date, expire_date, volume)
        VALUES (?, ?, ?, ?)
    """, (
        user_id,
        buy_date.strftime("%Y-%m-%d"),
        expire_date.strftime("%Y-%m-%d"),
        volume
    ))

    conn.commit()
    conn.close()


def get_user_subscriptions(user_id):

    conn = connect()
    cur = conn.cursor()

    cur.execute(
        "SELECT * FROM subscriptions WHERE user_id=?",
        (user_id,)
    )

    subs = cur.fetchall()

    conn.close()
    return subs
