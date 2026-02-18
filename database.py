import sqlite3
from datetime import datetime, timedelta

def get_connection():
    return sqlite3.connect("/tmp/bot.db", check_same_thread=False)

def create_tables():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        invited_by INTEGER,
        points INTEGER DEFAULT 0
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS subscriptions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        months INTEGER,
        start_date TEXT,
        end_date TEXT,
        config TEXT
    )
    """)

    conn.commit()
    conn.close()

def create_user(user_id, invited_by=None):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT id FROM users WHERE id=?", (user_id,))
    if not cursor.fetchone():
        cursor.execute(
            "INSERT INTO users (id, invited_by) VALUES (?, ?)",
            (user_id, invited_by)
        )

    conn.commit()
    conn.close()

def get_user(user_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE id=?", (user_id,))
    user = cursor.fetchone()
    conn.close()
    return user

def add_points(user_id, amount):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET points = points + ? WHERE id=?", (amount, user_id))
    conn.commit()
    conn.close()

def create_subscription(user_id, months):
    conn = get_connection()
    cursor = conn.cursor()

    start = datetime.now()
    end = start + timedelta(days=30 * months)
    config_text = f"WG-CONFIG-{user_id}-{int(start.timestamp())}"

    cursor.execute("""
        INSERT INTO subscriptions (user_id, months, start_date, end_date, config)
        VALUES (?, ?, ?, ?, ?)
    """, (user_id, months, start.isoformat(), end.isoformat(), config_text))

    conn.commit()
    conn.close()

def get_subs(user_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT months, start_date, end_date, config
        FROM subscriptions
        WHERE user_id=?
    """, (user_id,))

    data = cursor.fetchall()
    conn.close()
    return data
