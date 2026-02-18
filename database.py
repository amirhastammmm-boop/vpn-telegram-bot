import sqlite3
import random
import string


# ---------------- ساخت جدول ها ----------------

def create_tables():

    conn = sqlite3.connect("bot.db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS subscriptions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            buy_date TEXT,
            expire_date TEXT,
            volume TEXT,
            private_key TEXT,
            address TEXT,
            server_public_key TEXT,
            endpoint TEXT
        )
    """)

    conn.commit()
    conn.close()


# ---------------- جدول کاربران و امتیاز ----------------

def create_users_table():

    conn = sqlite3.connect("bot.db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            referral_code TEXT UNIQUE,
            invited_by INTEGER,
            points INTEGER DEFAULT 0
        )
    """)

    conn.commit()
    conn.close()


# ---------------- افزودن اشتراک ----------------

def add_subscription(data):

    conn = sqlite3.connect("bot.db")
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO subscriptions
        (user_id, buy_date, expire_date, volume,
         private_key, address, server_public_key, endpoint)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, data)

    conn.commit()
    conn.close()


# ---------------- گرفتن اشتراک های کاربر ----------------

def get_user_subscriptions(user_id):

    conn = sqlite3.connect("bot.db")
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM subscriptions WHERE user_id=?",
        (user_id,)
    )

    subs = cursor.fetchall()
    conn.close()

    return subs


# ---------------- سیستم رفرال ----------------

def generate_referral_code():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))


def add_user(user_id, referral_code=None):

    conn = sqlite3.connect("bot.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users WHERE user_id=?", (user_id,))
    user = cursor.fetchone()

    if user:
        conn.close()
        return

    my_code = generate_referral_code()
    invited_by = None

    if referral_code:
        cursor.execute("SELECT user_id FROM users WHERE referral_code=?", (referral_code,))
        inviter = cursor.fetchone()

        if inviter and inviter[0] != user_id:
            invited_by = inviter[0]

            cursor.execute(
                "UPDATE users SET points = points + 1 WHERE user_id=?",
                (invited_by,)
            )

    cursor.execute("""
        INSERT INTO users (user_id, referral_code, invited_by)
        VALUES (?, ?, ?)
    """, (user_id, my_code, invited_by))

    conn.commit()
    conn.close()


def get_user_points(user_id):

    conn = sqlite3.connect("bot.db")
    cursor = conn.cursor()

    cursor.execute("SELECT points FROM users WHERE user_id=?", (user_id,))
    result = cursor.fetchone()

    conn.close()

    return result[0] if result else 0
