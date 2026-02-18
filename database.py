import sqlite3

DB_NAME = "vpn.db"


# ---------- اتصال ----------
def connect():
    return sqlite3.connect(DB_NAME)


# ---------- ساخت جدول ها ----------
def create_tables():
    conn = connect()
    cursor = conn.cursor()

    # جدول کاربران
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER UNIQUE,
        referrer INTEGER DEFAULT NULL,
        points INTEGER DEFAULT 0
    )
    """)

    # جدول اشتراک ها
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS subscriptions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        sub_type TEXT,
        volume TEXT,
        status TEXT,
        config TEXT
    )
    """)

    # جدول زیرمجموعه ها
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS referrals (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        inviter INTEGER,
        invited INTEGER
    )
    """)

    conn.commit()
    conn.close()


# ---------- افزودن کاربر ----------
def add_user(user_id, referrer=None):
    conn = connect()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users WHERE user_id=?", (user_id,))
    user = cursor.fetchone()

    if not user:
        cursor.execute(
            "INSERT INTO users (user_id, referrer) VALUES (?, ?)",
            (user_id, referrer)
        )

        # ثبت زیرمجموعه
        if referrer:
            cursor.execute(
                "INSERT INTO referrals (inviter, invited) VALUES (?, ?)",
                (referrer, user_id)
            )

    conn.commit()
    conn.close()


# ---------- گرفتن امتیاز ----------
def get_points(user_id):
    conn = connect()
    cursor = conn.cursor()

    cursor.execute("SELECT points FROM users WHERE user_id=?", (user_id,))
    data = cursor.fetchone()

    conn.close()

    return data[0] if data else 0


# ---------- تعداد زیرمجموعه ----------
def get_referral_count(user_id):
    conn = connect()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM referrals WHERE inviter=?", (user_id,))
    count = cursor.fetchone()[0]

    conn.close()
    return count


# ---------- افزودن اشتراک ----------
def add_subscription(user_id, sub_type, volume, config):
    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO subscriptions (user_id, sub_type, volume, status, config)
    VALUES (?, ?, ?, ?, ?)
    """, (user_id, sub_type, volume, "فعال", config))

    conn.commit()
    conn.close()


# ---------- گرفتن اشتراک های کاربر ----------
def get_user_subscriptions(user_id):
    conn = connect()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM subscriptions WHERE user_id=?", (user_id,))
    data = cursor.fetchall()

    conn.close()
    return data
