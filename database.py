import sqlite3
import random
import string

DB_NAME = "bot.db"


# ---------------- اتصال ----------------

def get_conn():
    return sqlite3.connect(DB_NAME)


# ---------------- جدول اشتراک ----------------

def create_tables():

    conn = get_conn()
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


# ---------------- جدول کاربران ----------------

def create_users_table():

    conn = get_conn()
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


# ---------------- رفرال ----------------

def generate_referral_code():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))


def add_user(user_id, referral_code=None):

    conn = get_conn()
    cursor = conn.cursor()

    # اگر کاربر قبلا ثبت شده
    cursor.execute("SELECT * FROM users WHERE user_id=?", (user_id,))
    if cursor.fetchone():
        conn.close()
        return

    my_code = generate_referral_code()
    invited_by = None

    # بررسی کد رفرال
    if referral_code:
        cursor.execute(
            "SELECT user_id FROM users WHERE referral_code=?",
            (referral_code,)
        )
        inviter = cursor.fetchone()

        # جلوگیری از تقلب
        if inviter and inviter[0] != user_id:
            invited_by = inviter[0]

            # دادن امتیاز دعوت
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


# ---------------- امتیاز ----------------

def get_user_points(user_id):

    conn = get_conn()
    cursor = conn.cursor()

    cursor.execute("SELECT points FROM users WHERE user_id=?", (user_id,))
    row = cursor.fetchone()

    conn.close()

    return row[0] if row else 0


def add_points(user_id, amount):

    conn = get_conn()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE users
        SET points = points + ?
        WHERE user_id=?
    """, (amount, user_id))

    conn.commit()
    conn.close()


def remove_points(user_id, amount):

    conn = get_conn()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE users
        SET points = points - ?
        WHERE user_id=? AND points >= ?
    """, (amount, user_id, amount))

    conn.commit()
    conn.close()


# ---------------- دعوت کننده ----------------

def get_inviter(user_id):

    conn = get_conn()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT invited_by FROM users WHERE user_id=?
    """, (user_id,))

    row = cursor.fetchone()
    conn.close()

    return row[0] if row else None


# ---------------- گرفتن کد رفرال ----------------

def get_referral_code(user_id):

    conn = get_conn()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT referral_code FROM users WHERE user_id=?
    """, (user_id,))

    row = cursor.fetchone()
    conn.close()

    return row[0] if row else None


# ---------------- گرفتن اشتراک ها ----------------

def get_user_subscriptions(user_id):

    conn = get_conn()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM subscriptions
        WHERE user_id=?
    """, (user_id,))

    rows = cursor.fetchall()
    conn.close()

    return rows
