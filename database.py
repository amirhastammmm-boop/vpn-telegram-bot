import sqlite3

conn = sqlite3.connect("vpn.db", check_same_thread=False)
cursor = conn.cursor()

# ساخت جدول کاربران
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY
)
""")

# ساخت جدول اشتراک ها
cursor.execute("""
CREATE TABLE IF NOT EXISTS subscriptions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    sub_number TEXT,
    sub_type TEXT,
    buy_date TEXT,
    expire_date TEXT,
    total_gb INTEGER,
    used_gb INTEGER,
    status TEXT,
    config TEXT
)
""")

conn.commit()


# افزودن کاربر
def add_user(user_id):
    cursor.execute("INSERT OR IGNORE INTO users (user_id) VALUES (?)", (user_id,))
    conn.commit()


# گرفتن اشتراک های کاربر
def get_user_subscriptions(user_id):
    cursor.execute("SELECT * FROM subscriptions WHERE user_id=?", (user_id,))
    return cursor.fetchall()


# گرفتن اشتراک خاص
def get_subscription_by_id(sub_id, user_id):
    cursor.execute(
        "SELECT * FROM subscriptions WHERE id=? AND user_id=?",
        (sub_id, user_id)
    )
    return cursor.fetchone()


# فقط برای تست — افزودن اشتراک نمونه
def add_test_subscription(user_id):

    cursor.execute("""
    INSERT INTO subscriptions 
    (user_id, sub_number, sub_type, buy_date, expire_date, total_gb, used_gb, status, config)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        user_id,
        "2135081",
        "یک ماهه",
        "2026-02-09 20:23:19",
        "2026-03-09 20:23:19",
        37888,
        9946,
        "✅فعال",
        "نمونه کانفیگ VPN"
    ))

    conn.commit()
