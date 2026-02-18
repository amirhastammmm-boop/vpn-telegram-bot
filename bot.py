import logging
import sqlite3
import uuid
from datetime import datetime, timedelta

from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    ReplyKeyboardMarkup,
)
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

TOKEN = "8443993110:AAH08NXvjcKty2XBHH13ecD8l5giSCD-ZF4"

logging.basicConfig(level=logging.INFO)

conn = sqlite3.connect("database.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY,
    referral_code TEXT,
    invited_by TEXT,
    points INTEGER DEFAULT 0
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS subscriptions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    sub_code TEXT,
    expire_date TEXT
)
""")
conn.commit()


def main_menu():
    keyboard = [
        ["🛒 خرید اشتراک", "📦 اشتراک های من"],
        ["🎁 امتیاز ها", "📚 آموزش"],
        ["🆘 پشتیبانی"],
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    args = context.args

    cursor.execute("SELECT * FROM users WHERE user_id=?", (user_id,))
    user = cursor.fetchone()

    if not user:
        referral_code = str(uuid.uuid4())[:8]
        invited_by = args[0] if args else None

        cursor.execute(
            "INSERT INTO users (user_id, referral_code, invited_by) VALUES (?, ?, ?)",
            (user_id, referral_code, invited_by),
        )
        conn.commit()

        if invited_by:
            cursor.execute(
                "UPDATE users SET points = points + 1 WHERE referral_code=?",
                (invited_by,),
            )
            conn.commit()

    await update.message.reply_text(
        "به ربات Payydar VPN خوش اومدی 👋",
        reply_markup=main_menu()
    )


async def buy_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [
            InlineKeyboardButton("۱ ماهه", callback_data="buy_1"),
            InlineKeyboardButton("۲ ماهه", callback_data="buy_2"),
        ],
        [InlineKeyboardButton("۳ ماهه", callback_data="buy_3")],
    ]
    await update.message.reply_text(
        "پلن مورد نظر رو انتخاب کن:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


async def handle_buy(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    user_id = query.from_user.id
    months = int(query.data.split("_")[1])

    sub_code = str(uuid.uuid4())[:10]
    expire = datetime.now() + timedelta(days=30 * months)

    cursor.execute(
        "INSERT INTO subscriptions (user_id, sub_code, expire_date) VALUES (?, ?, ?)",
        (user_id, sub_code, expire.strftime("%Y-%m-%d")),
    )
    conn.commit()

    await query.edit_message_text(
        f"✅ اشتراک ساخته شد\n\n"
        f"کد اشتراک:\n{sub_code}\n\n"
        f"تاریخ انقضا: {expire.strftime('%Y-%m-%d')}"
    )


async def my_subs(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    cursor.execute(
        "SELECT sub_code, expire_date FROM subscriptions WHERE user_id=?",
        (user_id,),
    )
    subs = cursor.fetchall()

    if not subs:
        await update.message.reply_text("❌ شما اشتراکی ندارید.")
        return

    text = "📦 اشتراک های شما:\n\n"
    for s in subs:
        text += f"کد: {s[0]}\nانقضا: {s[1]}\n\n"

    await update.message.reply_text(text)


async def points_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    cursor.execute(
        "SELECT referral_code, points FROM users WHERE user_id=?",
        (user_id,),
    )
    data = cursor.fetchone()

    referral_code = data[0]
    points = data[1]

    text = f"""
🎁 امتیاز شما: {points}

کد رفرال شما:
{referral_code}

لینک دعوت شما:
https://t.me/PayydarVpn_robot?start={referral_code}

هر ۵ امتیاز = اشتراک رایگان
هر ۸ امتیاز = اشتراک ویژه
"""

    await update.message.reply_text(text)


async def send_guide(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📚 آموزش اتصال بعد از خرید ارسال می‌شود.")


async def support(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🆘 پشتیبانی: @Amnbytry")


def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.Regex("🛒 خرید اشتراک"), buy_menu))
    app.add_handler(MessageHandler(filters.Regex("📦 اشتراک های من"), my_subs))
    app.add_handler(MessageHandler(filters.Regex("🎁 امتیاز ها"), points_menu))
    app.add_handler(MessageHandler(filters.Regex("📚 آموزش"), send_guide))
    app.add_handler(MessageHandler(filters.Regex("🆘 پشتیبانی"), support))

    app.add_handler(CallbackQueryHandler(handle_buy, pattern="buy_"))

    app.run_polling()


if __name__ == "__main__":
    main()
