import sqlite3


# ---------------- اتصال دیتابیس ----------------

def get_connection():
    return sqlite3.connect("bot.db")


# ---------------- ساخت جدول ها ----------------

def create_tables():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS subscriptions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
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


# ---------------- افزودن اشتراک ----------------

def add_subscription(
        user_id,
        buy_date,
        expire_date,
        volume,
        private_key,
        address,
        server_public_key,
        endpoint
):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO subscriptions
        (user_id, buy_date, expire_date, volume,
         private_key, address, server_public_key, endpoint)

        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        user_id,
        buy_date,
        expire_date,
        volume,
        private_key,
        address,
        server_public_key,
        endpoint
    ))

    conn.commit()
    conn.close()


# ---------------- گرفتن همه اشتراک های کاربر ----------------

def get_user_subscriptions(user_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM subscriptions
        WHERE user_id=?
        ORDER BY id DESC
    """, (user_id,))

    subs = cursor.fetchall()

    conn.close()
    return subs


# ---------------- گرفتن یک اشتراک خاص ----------------

def get_subscription(user_id, sub_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM subscriptions
        WHERE user_id=? AND id=?
    """, (user_id, sub_id))

    sub = cursor.fetchone()

    conn.close()
    return sub
