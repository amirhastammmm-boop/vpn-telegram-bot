import sqlite3
from datetime import datetime, timedelta

from telegram import *
from telegram.ext import *

from config import TOKEN, BOT_USERNAME, PAYMENT_LINKS
from wireguard import create_wireguard_config

# ===== دیتابیس =====
conn = sqlite3.connect("database.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users(
    user_id INTEGER PRIMARY KEY,
    points INTEGER DEFAULT 0,
    inviter INTEGER,
    invited_count INTEGER DEFAULT 0
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS subscriptions(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    volume INTEGER,
    expire TEXT,
    created TEXT
)
""")

conn.commit()


# ===== منوی اصلی =====
def main_menu():
    keyboard = [
        ["🛒 خرید اشتراک", "📦 اشتراک های من"],
        ["⭐ امتیاز من", "📚 آموزش"],
        ["🆘 پشتیبانی"]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)


# ===== ساخت اشتراک =====
def create_subscription(user_id, volume, days):

    expire = datetime.now() + timedelta(days=days)

    cursor.execute("""
    INSERT INTO subscriptions(user_id,volume,expire,created)
    VALUES (?,?,?,?)
    """, (
        user_id,
        volume,
        expire.strftime("%Y-%m-%d"),
        datetime.now().strftime("%Y-%m-%d")
    ))

    conn.commit()

    return create_wireguard_config(user_id)


# ===== سیستم رفرال ضد تقلب =====
def reward_inviter(user_id, months):

    cursor.execute("SELECT inviter FROM users WHERE user_id=?", (user_id,))
    inviter = cursor.fetchone()

    if inviter and inviter[0]:

        reward = months
        cursor.execute(
            "UPDATE users SET points = points + ? WHERE user_id=?",
            (reward, inviter[0])
        )
        conn.commit()


# ===== start =====
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_id = update.effective_user.id
    inviter = None

    if context.args:
        try:
            inviter = int(context.args[0])
        except:
            inviter = None

    cursor.execute("SELECT user_id FROM users WHERE user_id=?", (user_id,))
    exists = cursor.fetchone()

    if not exists:

        if inviter == user_id:
            inviter = None

        cursor.execute(
            "INSERT INTO users(user_id,inviter) VALUES (?,?)",
            (user_id, inviter)
        )

        if inviter:
            cursor.execute(
                "UPDATE users SET invited_count = invited_count + 1 WHERE user_id=?",
                (inviter,)
            )

            cursor.execute("""
            UPDATE users
            SET points = points + 1
            WHERE user_id=? AND invited_count % 5 = 0
            """, (inviter,))

        conn.commit()

    await update.message.reply_text("خوش اومدی ❤️", reply_markup=main_menu())


# ===== خرید اشتراک =====
async def buy_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):

    keyboard = [
        [InlineKeyboardButton("۱ ماهه ۳۳GB - ۱۴۰", callback_data="sub1")],
        [InlineKeyboardButton("۲ ماهه ۷۱GB - ۲۸۰", callback_data="sub2")],
        [InlineKeyboardButton("۳ ماهه ۱۱۰GB - ۴۰۰", callback_data="sub3")],
        [InlineKeyboardButton("🎁 خرید با امتیاز", callback_data="point_buy")]
    ]

    await update.message.reply_text(
        "پلن مورد نظر را انتخاب کن 👇",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


# ===== اشتراک های من =====
async def my_subs(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_id = update.effective_user.id

    cursor.execute("SELECT volume,expire,created FROM subscriptions WHERE user_id=?", (user_id,))
    subs = cursor.fetchall()

    if not subs:
        await update.message.reply_text("اشتراکی نداری")
        return

    text = "📦 اشتراک های شما:\n\n"

    for s in subs:
        text += f"""
حجم: {s[0]} گیگ
خرید: {s[2]}
انقضا: {s[1]}
-------------
"""

    await update.message.reply_text(text)


# ===== امتیاز =====
async def points(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_id = update.effective_user.id

    cursor.execute("SELECT points FROM users WHERE user_id=?", (user_id,))
    p = cursor.fetchone()[0]

    ref = f"https://t.me/{BOT_USERNAME}?start={user_id}"

    text = f"""
⭐ امتیاز شما: {p}

🔗 لینک دعوت:
{ref}

هر 5 دعوت = 1 امتیاز  
خرید زیرمجموعه:
1 ماه = 1 امتیاز
2 ماه = 2 امتیاز
3 ماه = 3 امتیاز

🎁 5 امتیاز = اشتراک 1 ماه  
🎁 8 امتیاز = اشتراک 2 ماه
"""

    await update.message.reply_text(text)


# ===== آموزش =====
async def learn(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("فایل را داخل برنامه WireGuard ایمپورت کن")


# ===== پشتیبانی =====
async def support(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("جهت پشتیبانی پیام دهید:\n633464148")


# ===== دکمه ها =====
async def buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    await query.answer()

    user_id = query.from_user.id

    if query.data in PAYMENT_LINKS:
        await query.message.reply_text(f"لینک پرداخت:\n{PAYMENT_LINKS[query.data]}")

        if query.data == "sub1":
            config = create_subscription(user_id, 33, 30)
            reward_inviter(user_id, 1)

        elif query.data == "sub2":
            config = create_subscription(user_id, 71, 60)
            reward_inviter(user_id, 2)

        elif query.data == "sub3":
            config = create_subscription(user_id, 110, 90)
            reward_inviter(user_id, 3)

        await query.message.reply_text(config)

    elif query.data == "point_buy":

        cursor.execute("SELECT points FROM users WHERE user_id=?", (user_id,))
        p = cursor.fetchone()[0]

        if p >= 8:
            config = create_subscription(user_id, 71, 60)
            cursor.execute("UPDATE users SET points=points-8 WHERE user_id=?", (user_id,))
            await query.message.reply_text(config)

        elif p >= 5:
            config = create_subscription(user_id, 33, 30)
            cursor.execute("UPDATE users SET points=points-5 WHERE user_id=?", (user_id,))
            await query.message.reply_text(config)

        else:
            await query.message.reply_text("امتیاز کافی نیست")

        conn.commit()


# ===== هندل پیام =====
async def handler(update: Update, context: ContextTypes.DEFAULT_TYPE):

    text = update.message.text

    if text == "🛒 خرید اشتراک":
        await buy_menu(update, context)

    elif text == "📦 اشتراک های من":
        await my_subs(update, context)

    elif text == "⭐ امتیاز من":
        await points(update, context)

    elif text == "📚 آموزش":
        await learn(update, context)

    elif text == "🆘 پشتیبانی":
        await support(update, context)


# ===== اجرا =====
app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handler))
app.add_handler(CallbackQueryHandler(buttons))

print("Bot Running...")
app.run_polling()
