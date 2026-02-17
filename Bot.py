import sqlite3
import random
import string
from datetime import datetime, timedelta

from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    ReplyKeyboardMarkup
)
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ContextTypes,
    filters
)

# ===== تنظیمات =====
TOKEN = "PUT_YOUR_TOKEN_HERE"
BOT_USERNAME = "PayydarVpn_robot"

# ===== دیتابیس =====
conn = sqlite3.connect("database.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users(
    user_id INTEGER PRIMARY KEY,
    points INTEGER DEFAULT 0,
    inviter INTEGER
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS subscriptions(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    volume INTEGER,
    expire TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS referrals(
    inviter INTEGER,
    invited INTEGER UNIQUE,
    purchased INTEGER DEFAULT 0
)
""")

conn.commit()


# ===== ساخت کانفیگ فیک =====
def generate_config():
    return "vpn://" + ''.join(random.choices(string.ascii_letters + string.digits, k=25))


# ===== ساخت اشتراک =====
def create_subscription(user_id, volume, days):
    expire = datetime.now() + timedelta(days=days)

    cursor.execute(
        "INSERT INTO subscriptions (user_id, volume, expire) VALUES (?,?,?)",
        (user_id, volume, expire.strftime("%Y-%m-%d"))
    )
    conn.commit()

    return generate_config()


# ===== امتیاز خرید زیرمجموعه =====
def reward_inviter(user_id, month):
    cursor.execute("SELECT inviter FROM users WHERE user_id=?", (user_id,))
    res = cursor.fetchone()

    if not res or not res[0]:
        return

    inviter = res[0]

    cursor.execute(
        "SELECT purchased FROM referrals WHERE invited=?",
        (user_id,)
    )
    data = cursor.fetchone()

    if data and data[0] == 0:
        cursor.execute(
            "UPDATE users SET points = points + ? WHERE user_id=?",
            (month, inviter)
        )

        cursor.execute(
            "UPDATE referrals SET purchased=1 WHERE invited=?",
            (user_id,)
        )

        conn.commit()


# ===== کیبورد اصلی =====
def main_menu():
    keyboard = [
        ["📦 اشتراک های من"],
        ["⭐ امتیاز من"]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)


# ===== start =====
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    if not cursor.execute("SELECT * FROM users WHERE user_id=?", (user_id,)).fetchone():

        inviter = None

        if context.args:
            ref = int(context.args[0])

            if ref != user_id:
                inviter = ref

        cursor.execute(
            "INSERT INTO users (user_id, inviter) VALUES (?,?)",
            (user_id, inviter)
        )

        if inviter:
            cursor.execute(
                "INSERT OR IGNORE INTO referrals (inviter, invited) VALUES (?,?)",
                (inviter, user_id)
            )

            cursor.execute(
                "UPDATE users SET points = points + 1 WHERE user_id=?",
                (inviter,)
            )

        conn.commit()

    await update.message.reply_text(
        "خوش اومدی 👋",
        reply_markup=main_menu()
    )


# ===== اشتراک های من =====
async def my_subs(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    cursor.execute(
        "SELECT volume, expire FROM subscriptions WHERE user_id=?",
        (user_id,)
    )

    subs = cursor.fetchall()

    text = ""

    if subs:
        for s in subs:
            text += f"📦 {s[0]} گیگ\n⏳ تا {s[1]}\n\n"
    else:
        text = "❌ اشتراکی نداری"

    keyboard = [
        [
            InlineKeyboardButton("1 ماهه", callback_data="sub1"),
            InlineKeyboardButton("2 ماهه", callback_data="sub2"),
            InlineKeyboardButton("3 ماهه", callback_data="sub3")
        ],
        [InlineKeyboardButton("خرید با امتیاز", callback_data="point_buy")]
    ]

    await update.message.reply_text(
        text,
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


# ===== امتیاز =====
async def points(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    cursor.execute("SELECT points FROM users WHERE user_id=?", (user_id,))
    p = cursor.fetchone()[0]

    ref_link = f"https://t.me/{BOT_USERNAME}?start={user_id}"

    text = f"""
⭐ امتیاز شما: {p}

👥 لینک دعوت شما:
{ref_link}

قوانین:
هر دعوت = 1 امتیاز
خرید زیرمجموعه:
1 ماهه = 1 امتیاز
2 ماهه = 2 امتیاز
3 ماهه = 3 امتیاز
"""

    await update.message.reply_text(text)


# ===== دکمه ها =====
async def buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    user_id = query.from_user.id

    if query.data == "sub1":
        await query.message.reply_text("در حال انتقال به پرداخت...")
        config = create_subscription(user_id, 33, 30)
        reward_inviter(user_id, 1)
        await query.message.reply_text(f"کانفیگ شما:\n{config}")

    elif query.data == "sub2":
        await query.message.reply_text("در حال انتقال به پرداخت...")
        config = create_subscription(user_id, 71, 60)
        reward_inviter(user_id, 2)
        await query.message.reply_text(f"کانفیگ شما:\n{config}")

    elif query.data == "sub3":
        await query.message.reply_text("در حال انتقال به پرداخت...")
        config = create_subscription(user_id, 110, 90)
        reward_inviter(user_id, 3)
        await query.message.reply_text(f"کانفیگ شما:\n{config}")

    elif query.data == "point_buy":

        cursor.execute("SELECT points FROM users WHERE user_id=?", (user_id,))
        p = cursor.fetchone()[0]

        if p >= 10:
            config = create_subscription(user_id, 71, 60)
            cursor.execute("UPDATE users SET points = points - 10 WHERE user_id=?", (user_id,))
            conn.commit()
            await query.message.reply_text(config)

        elif p >= 5:
            config = create_subscription(user_id, 33, 30)
            cursor.execute("UPDATE users SET points = points - 5 WHERE user_id=?", (user_id,))
            conn.commit()
            await query.message.reply_text(config)

        else:
            await query.message.reply_text("❌ امتیاز کافی نیست")


# ===== هندل پیام =====
async def handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    if text == "📦 اشتراک های من":
        await my_subs(update, context)

    elif text == "⭐ امتیاز من":
        await points(update, context)


# ===== اجرا =====
app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handler))
app.add_handler(CallbackQueryHandler(buttons))

print("Bot is running...")
app.run_polling()
