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
    referrer INTEGER
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

# ===== کیبورد اصلی =====
def main_keyboard():
    keyboard = [
        ["📦 اشتراک های من"],
        ["⭐ امتیاز من", "🆘 پشتیبانی"]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

# ===== ثبت کاربر =====
def add_user(user_id, referrer=None):
    cursor.execute("SELECT * FROM users WHERE user_id=?", (user_id,))
    if cursor.fetchone() is None:
        cursor.execute("INSERT INTO users(user_id, referrer) VALUES(?,?)",
                       (user_id, referrer))
        db.commit()

        if referrer:
            cursor.execute("UPDATE users SET score = score + 1 WHERE user_id=?",
                           (referrer,))
            db.commit()

# ===== امتیاز خرید =====
def add_purchase_score(user_id, plan):
    cursor.execute("SELECT referrer FROM users WHERE user_id=?", (user_id,))
    ref = cursor.fetchone()

    if ref and ref[0]:
        if plan == 1:
            score = 1
        elif plan == 2:
            score = 2
        else:
            score = 3

        cursor.execute("UPDATE users SET score = score + ? WHERE user_id=?",
                       (score, ref[0]))
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

    cursor.execute("INSERT INTO subs VALUES (?,?,?,?)",
                   (user_id, plan, expire, volume))
    db.commit()

    add_purchase_score(user_id, plan)

# ===== start =====
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_id = update.effective_user.id

    ref = None
    if context.args:
        ref = int(context.args[0])

    add_user(user_id, ref)

    await update.message.reply_text(
        "به ربات خوش اومدی 👋",
        reply_markup=main_keyboard()
    )

# ===== اشتراک ها =====
async def my_sub(update: Update, context: ContextTypes.DEFAULT_TYPE):

    keyboard = [
        [
            InlineKeyboardButton("۱ ماهه ۳۳GB - ۱۳۵", callback_data="plan1"),
            InlineKeyboardButton("۲ ماهه ۷۱GB - ۲۷۰", callback_data="plan2")
        ],
        [
            InlineKeyboardButton("۳ ماهه ۱۱۰GB - ۵۴۰", callback_data="plan3")
        ],
        [
            InlineKeyboardButton("🎁 خرید با امتیاز", callback_data="score_buy")
        ]
    ]

    await update.message.reply_text(
        "پلن مورد نظر را انتخاب کن",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

# ===== مدیریت پلن =====
async def plan_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    user_id = query.from_user.id
    await query.answer()

    # ===== خرید عادی =====
    if query.data.startswith("plan"):

        plan = int(query.data[-1])

        # اینجا باید لینک پرداخت بزاری
        await query.message.reply_text("درگاه پرداخت (بعداً وصل میشه)")

        # فعلاً تستی اشتراک میسازیم
        create_sub(user_id, plan)

        await query.message.reply_text("✅ اشتراک فعال شد")

    # ===== خرید با امتیاز =====
    if query.data == "score_buy":

        cursor.execute("SELECT score FROM users WHERE user_id=?", (user_id,))
        score = cursor.fetchone()[0]

        if score >= 10:
            create_sub(user_id, 2)
            cursor.execute("UPDATE users SET score = score - 10 WHERE user_id=?", (user_id,))
            db.commit()
            await query.message.reply_text("اشتراک ۲ ماهه فعال شد")

        elif score >= 5:
            create_sub(user_id, 1)
            cursor.execute("UPDATE users SET score = score - 5 WHERE user_id=?", (user_id,))
            db.commit()
            await query.message.reply_text("اشتراک ۱ ماهه فعال شد")

        else:
            await query.message.reply_text("امتیاز کافی نداری")

# ===== نمایش اشتراک =====
async def show_sub(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_id = update.effective_user.id

    cursor.execute("SELECT * FROM subs WHERE user_id=?", (user_id,))
    data = cursor.fetchall()

    if not data:
        await update.message.reply_text("اشتراکی نداری")
        return

    text = "📦 اشتراک های شما:\n\n"

    for sub in data:
        expire = datetime.datetime.fromisoformat(sub[2])
        remain = expire - datetime.datetime.now()

        text += f"""
پلن {sub[1]} ماهه
حجم {sub[3]} گیگ
باقی مانده {remain.days} روز
"""

    await update.message.reply_text(text)

# ===== امتیاز =====
async def score(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_id = update.effective_user.id

    cursor.execute("SELECT score FROM users WHERE user_id=?", (user_id,))
    score = cursor.fetchone()[0]

    referral = f"https://t.me/YOURBOT?start={user_id}"

    text = f"""
⭐ امتیاز شما: {score}

👥 لینک دعوت:
{referral}

هر دعوت = ۱ امتیاز
خرید زیرمجموعه:
۱ ماهه = ۱ امتیاز
۲ ماهه = ۲ امتیاز
۳ ماهه = ۳ امتیاز
"""

    await update.message.reply_text(text)

# ===== اجرا =====
def main():

    app = ApplicationBuilder().token(config.BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT("📦 اشتراک های من"), my_sub))
    app.add_handler(MessageHandler(filters.TEXT("⭐ امتیاز من"), score))
    app.add_handler(MessageHandler(filters.TEXT("📦 اشتراک های من"), show_sub))

    app.add_handler(CallbackQueryHandler(plan_handler))

    app.run_polling()

if __name__ == "__main__":
    main()
