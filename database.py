import sqlite3
from datetime import datetime, timedelta


def connect():
    return sqlite3.connect("data.db")


def create_tables():
    conn = connect()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS users(
        user_id INTEGER PRIMARY KEY,
        points INTEGER DEFAULT 0
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS subscriptions(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        months INTEGER,
        start TEXT,
        end TEXT
    )
    """)

    conn.commit()
    conn.close()


def add_user(user_id):
    conn = connect()
    cur = conn.cursor()

    cur.execute(
        "INSERT OR IGNORE INTO users(user_id) VALUES(?)",
        (user_id,)
    )

    conn.commit()
    conn.close()


def create_subscription(user_id, months):

    add_user(user_id)

    start = datetime.now()
    end = start + timedelta(days=30 * months)

    conn = connect()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO subscriptions(user_id, months, start, end)
        VALUES(?,?,?,?)
    """, (
        user_id,
        months,
        start.strftime("%Y-%m-%d"),
        end.strftime("%Y-%m-%d")
    ))

    conn.commit()
    conn.close()


def get_user_subscriptions(user_id):

    conn = connect()
    cur = conn.cursor()

    cur.execute(
        "SELECT months,start,end FROM subscriptions WHERE user_id=?",
        (user_id,)
    )

    rows = cur.fetchall()
    conn.close()

    result = []

    for r in rows:
        result.append({
            "months": r[0],
            "start": r[1],
            "end": r[2]
        })

    return result


def get_user_points(user_id):

    add_user(user_id)

    conn = connect()
    cur = conn.cursor()

    cur.execute(
        "SELECT points FROM users WHERE user_id=?",
        (user_id,)
    )

    row = cur.fetchone()
    conn.close()

    return row[0] if row else 0


def use_points(user_id, amount):

    add_user(user_id)

    conn = connect()
    cur = conn.cursor()

    cur.execute(
        "SELECT points FROM users WHERE user_id=?",
        (user_id,)
    )

    row = cur.fetchone()

    if not row:
        conn.close()
        return False

    points = row[0]

    if points < amount:
        conn.close()
        return False

    cur.execute(
        "UPDATE users SET points = points - ? WHERE user_id=?",
        (amount, user_id)
    )

    conn.commit()
    conn.close()

    return True
