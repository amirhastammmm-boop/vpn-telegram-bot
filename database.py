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
    invited INTEGER UNIQUE
)
""")

conn.commit()


# اضافه کردن کاربر
def add_user(user_id, inviter=None):

    cursor.execute("SELECT * FROM users WHERE user_id=?", (user_id,))
    if cursor.fetchone():
        return

    cursor.execute(
        "INSERT INTO users (user_id, inviter) VALUES (?,?)",
        (user_id, inviter)
    )

    if inviter:
        cursor.execute(
            "INSERT OR IGNORE INTO referrals VALUES (?,?)",
            (inviter, user_id)
        )

    conn.commit()


# گرفتن امتیاز
def get_points(user_id):
    cursor.execute("SELECT points FROM users WHERE user_id=?", (user_id,))
    data = cursor.fetchone()
    return data[0] if data else 0


# تعداد زیرمجموعه
def get_ref_count(user_id):
    cursor.execute("SELECT COUNT(*) FROM referrals WHERE inviter=?", (user_id,))
    return cursor.fetchone()[0]
