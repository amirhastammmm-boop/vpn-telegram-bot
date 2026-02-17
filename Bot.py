import sqlite3
import random
import string
from datetime import datetime, timedelta

from config import TOKEN, BOT_USERNAME, PAYMENT_LINKS

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

# ================= DATABASE =================

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

# ================= CONFIG GENERATOR =================

def generate_config():
    return "vpn://" + ''.join(random.choices(string.ascii_letters + string.digits, k=30))

# ================= CREATE SUB =================

def create_subscription(user_id, volume, days):
    expire = datetime.now() + timedelta(days=days)

    cursor.execute(
        "INSERT INTO subscriptions VALUES(NULL,?,?,?)",
        (user_id, volume, expire.strftime("%Y-%m-%d"))
    )
    conn.commit()

    return generate_config()

# ================= REFERRAL REWARD =================

def reward_inviter(user_id, month):
    cursor.execute("SELECT inviter FROM users WHERE user_id=?", (user_id,))
    res = cursor.fetchone()

    if not res or not res[0]:
        return

    inviter = res[0]

    cursor.execute("SELECT purchased FROM referrals WHERE invited=?", (user_id,))
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

# ================= MAIN KEYBOARD =================

def main_menu():
    keyboard = [
        ["📦 اشتراک های من"],
        ["⭐ امتیاز من"]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

# ================= START =================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    if not cursor.execute("SELECT * FROM users WHERE user_id=?", (user_id,)).fetchone():

        inviter = None

        if context.args:
            ref = int(context.args[0])
            if ref != user_id:
                inviter = ref

        cursor.execute("INSERT INTO users VALUES(?,?,?)", (user_id, 0, inviter))

        if inviter:
            cursor.execute(
                "INSERT OR IGNORE INTO referrals VALUES(?,?,0)",
                (inviter, user_id)
            )

        conn.commit()

    await update.message.reply_text("خوش اومدی 👋", reply_markup=main_menu())

# ================= SHOW SUBS =================

async def my_subs(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_id = update.effective_user.id

    cursor.execute("SELECT volume, expire FROM subscriptions WHERE user_id=?", (user_id,))
    subs = cursor.fetchall()

    text = "📦 اشتراک های شما:\n\n"

    if subs:
        for s in subs:
            expire = datetime.strptime(s[1], "%Y-%m-%d")
            left = (expire - datetime.now()).days
            text += f"🔹 {s[0]} گیگ | {left} روز باقی مانده\n"
    else:
        text += "❌ اشتراکی نداری\n"

    keyboard = [
        [InlineKeyboardButton("1 ماهه 33GB - 135T", callback_data="sub1")],
        [InlineKeyboardButton("2 ماهه 71GB - 270T", callback_data="sub2")],
        [InlineKeyboardButton("3 ماهه 110GB - 540T", callback_data="sub3")],
        [InlineKeyboardButton("خرید با امتیاز", callback_data="point_buy")]
    ]

    await update.message.reply_text(text, reply_markup=InlineKeyboardMarkup(keyboard))

# ================= POINTS =================

async def points(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_id = update.effective_user.id

    cursor.execute("SELECT points FROM users WHERE user_id=?", (user_id,))
    p = cursor.fetchone()[0]

    ref_link = f"https://t.me/{BOT_USERNAME}?start={user_id}"

    text = f"""
⭐ امتیاز شما: {p}

🔗 لینک دعوت:
{ref_link}

📌 قوانین:
هر 5 دعوت = 1 امتیاز
خرید زیرمجموعه:
1 ماهه = 1 امتیاز
2 ماهه = 2 امتیاز
3 ماهه = 3 امتیاز
"""

    await update.message.reply_text(text)

# ================= BUTTON HANDLER =================

async def buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    await query.answer()

    user_id = query.from_user.id

    if query.data in ["sub1","sub2","sub3"]:
        link = PAYMENT_LINKS[query.data]

        await query.message.reply_text(f"لینک پرداخت:\n{link}")

    elif query.data == "point_buy":

        cursor.execute("SELECT points FROM users WHERE user_id=?", (user_id,))
        p = cursor.fetchone()[0]

        if p >= 10:
            config = create_subscription(user_id,71,60)
            cursor.execute("UPDATE users SET points = points - 10 WHERE user_id=?", (user_id,))
            conn.commit()
            await query.message.reply_text(f"✅ اشتراک فعال شد\n{config}")

        elif p >= 5:
            config = create_subscription(user_id,33,30)
            cursor.execute("UPDATE users SET points = points - 5 WHERE user_id=?", (user_id,))
            conn.commit()
            await query.message.reply_text(f"✅ اشتراک فعال شد\n{config}")

        else:
            await query.message.reply_text("❌ امتیاز کافی نیست")

# ================= MESSAGE HANDLER =================

async def handler(update: Update, context: ContextTypes.DEFAULT_TYPE):

    text = update.message.text

    if text == "📦 اشتراک های من":
        await my_subs(update, context)

    elif text == "⭐ امتیاز من":
        await points(update, context)

# ================= RUN =================

if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handler))
    app.add_handler(CallbackQueryHandler(buttons))

    print("Bot Running...")
    app.run_polling()
