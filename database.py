import sqlite3

conn = sqlite3.connect("bot.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users(
    user_id INTEGER PRIMARY KEY,
    inviter INTEGER,
    points INTEGER DEFAULT 0
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS referrals(
    inviter INTEGER,
    invited INTEGER
)
""")

conn.commit()


def add_user(user_id, inviter=None):
    cursor.execute("SELECT user_id FROM users WHERE user_id=?", (user_id,))
    if cursor.fetchone() is None:
        cursor.execute("INSERT INTO users (user_id, inviter) VALUES (?,?)", (user_id, inviter))
        conn.commit()

        if inviter:
            cursor.execute("INSERT INTO referrals VALUES (?,?)", (inviter, user_id))
            conn.commit()


def get_points(user_id):
    cursor.execute("SELECT points FROM users WHERE user_id=?", (user_id,))
    result = cursor.fetchone()
    return result[0] if result else 0


def add_points(user_id, amount):
    cursor.execute("UPDATE users SET points = points + ? WHERE user_id=?", (amount, user_id))
    conn.commit()


def get_ref_count(user_id):
    cursor.execute("SELECT COUNT(*) FROM referrals WHERE inviter=?", (user_id,))
    return cursor.fetchone()[0]
