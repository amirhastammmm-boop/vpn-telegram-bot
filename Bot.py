from telegram import *
from telegram.ext import *
import config
import sqlite3
import datetime

# ===== دیتابیس =====
db = sqlite3.connect("bot.db", check_same_thread=False)
cursor = db.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users(
    user_id INTEGER PRIMARY KEY,
    score INTEGER DEFAULT 0,
    referrer INTEGER,
    invited INTEGER DEFAULT 0
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS subs(
    user_id INTEGER,
    plan INTEGER,
    expire TEXT,
    volume INTEGER
)
""")

db.commit()


# ===== کیبورد =====
def main_keyboard():
    keyboard = [
        ["📦 اشتراک های من"],
        ["⭐ امتیاز من"],
        ["🎁 خرید با امتیاز"]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)


# ===== گرفتن امتیاز امن =====
def get_score(user_id):
    cursor.execute("SELECT score FROM users WHERE user_id=?", (user_id,))
    data = cursor.fetchone()
    return data[0] if data else 0


# ===== ثبت کاربر + ضد تقلب =====
def add_user(user_id, referrer=None):

    cursor.execute("SELECT * FROM users WHERE user_id=?", (user_id,))
    if cursor.fetchone():
        return

    if referrer == user_id:
        referrer = None

    cursor.execute(
        "INSERT INTO users (user_id, referrer) VALUES (?,?)",
        (user_id, referrer)
    )

    # امتیاز دعوت
    if referrer:

        cursor.execute("SELECT invited FROM users WHERE user_id=?", (user_id,))
        invited = cursor.fetchone()

        if invited is None or invited[0] == 0:

            cursor.execute(
                "UPDATE users SET score = score + 1 WHERE user_id=?",
                (referrer,)
            )

            cursor.execute(
                "UPDATE users SET invited = 1 WHERE user_id=?",
                (user_id,)
            )

    db.commit()


# ===== امتیاز خرید زیرمجموعه =====
def add_purchase_score(user_id, plan):

    cursor.execute("SELECT referrer FROM users WHERE user_id=?", (user_id,))
    ref = cursor.fetchone()

    if not ref or not ref[0]:
        return

    score = plan
    cursor.execute(
        "UPDATE users SET score = score + ? WHERE user_id=?",
        (score, ref[0])
    )

    db.commit()


# ===== ساخت اشتراک =====
def create_sub(user_id, plan):

    if plan == 1:
        days = 30
        volume = 33
    elif plan == 2:
        days = 60
        volume = 71
    else:
        days = 90
        volume = 110

    expire = datetime.datetime.now() + datetime.timedelta(days=days)

    cursor.execute(
        "INSERT INTO subs VALUES (?,?,?,?)",
        (user_id, plan, expire.strftime("%Y-%m-%d"), volume)
    )

    db.commit()
    add_purchase_score(user_id, plan)


# ===== استارت =====
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_id = update.effective_user.id
    ref = None

    if context.args:
        try:
            ref = int(context.args[0])
        except:
            pass

    add_user(user_id, ref)

    await update.message.reply_text(
        "👋 خوش اومدی",
        reply_markup=main_keyboard()
    )


# ===== نمایش اشتراک =====
async def show_sub(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_id = update.effective_user.id

    cursor.execute("SELECT * FROM subs WHERE user_id=?", (user_id,))
    data = cursor.fetchall()

    if not data:
        await update.message.reply_text("❌ اشتراکی نداری")
        return

    text = "📦 اشتراک های شما:\n\n"

    for sub in data:
        expire = datetime.datetime.strptime(sub[2], "%Y-%m-%d")
        remain = expire - datetime.datetime.now()

        text += f"""
پلن {sub[1]} ماهه
حجم {sub[3]} گیگ
باقی مانده {remain.days} روز
"""

    await update.message.reply_text(text)


# ===== نمایش امتیاز =====
async def score(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_id = update.effective_user.id
    sc = get_score(user_id)

    referral = f"https://t.me/{config.BOT_USERNAME}?start={user_id}"

    text = f"""
⭐ امتیاز شما: {sc}

👥 لینک دعوت شما:
{referral}

هر دعوت = ۱ امتیاز
۱ ماه = ۵ امتیاز
۲ ماه = ۱۰ امتیاز
"""

    await update.message.reply_text(text)


# ===== خرید با امتیاز =====
async def buy_with_score(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_id = update.effective_user.id
    sc = get_score(user_id)

    if sc >= 10:

        create_sub(user_id, 2)

        cursor.execute(
            "UPDATE users SET score = score - 10 WHERE user_id=?",
            (user_id,)
        )
        db.commit()

        await update.message.reply_text("✅ اشتراک ۲ ماهه فعال شد")

    elif sc >= 5:

        create_sub(user_id, 1)

        cursor.execute(
            "UPDATE users SET score = score - 5 WHERE user_id=?",
            (user_id,)
        )
        db.commit()

        await update.message.reply_text("✅ اشتراک ۱ ماهه فعال شد")

    else:
        await update.message.reply_text("❌ امتیاز کافی نداری")


# ===== مدیریت پیام =====
async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):

    text = update.message.text

    if text == "📦 اشتراک های من":
        await show_sub(update, context)

    elif text == "⭐ امتیاز من":
        await score(update, context)

    elif text == "🎁 خرید با امتیاز":
        await buy_with_score(update, context)


# ===== اجرا =====
def main():

    app = ApplicationBuilder().token(config.TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message_handler))

    print("Bot Started...")
    app.run_polling()


if __name__ == "__main__":
    main()
