from telegram import ReplyKeyboardMarkup, Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

from config import TOKEN, ADMIN_ID
from database import add_user, get_user
from wireguard import create_wireguard_config
from payments import PAYMENT_LINK


# ===== منو اصلی =====
main_menu = ReplyKeyboardMarkup([
    ["📦 اشتراک های من", "💳 خرید اشتراک"],
    ["🏆 امتیاز های من", "📚 آموزش ربات"],
    ["🛠 پشتیبانی"]
], resize_keyboard=True)


# ===== استارت =====
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_id = update.effective_user.id
    add_user(user_id)

    await update.message.reply_text(
        "👋 به ربات فروش VPN خوش اومدی",
        reply_markup=main_menu
    )


# ===== اشتراک های من =====
async def my_subscription(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user = get_user(update.effective_user.id)

    await update.message.reply_text(
        f"📦 وضعیت اشتراک شما:\n\n{user[1]}"
    )


# ===== خرید اشتراک =====
async def buy_subscription(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(
        f"💳 برای خرید اشتراک روی لینک زیر بزن:\n{PAYMENT_LINK}\n\nبعد پرداخت /config رو بزن"
    )


# ===== ساخت کانفیگ =====
async def send_config(update: Update, context: ContextTypes.DEFAULT_TYPE):

    config = create_wireguard_config(update.effective_user.id)

    await update.message.reply_text(config)


# ===== امتیاز =====
async def my_points(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user = get_user(update.effective_user.id)

    await update.message.reply_text(
        f"🏆 امتیاز شما: {user[2]}"
    )


# ===== آموزش =====
async def tutorial(update: Update, context: ContextTypes.DEFAULT_TYPE):

    text = """
📚 آموزش اتصال VPN

1️⃣ برنامه WireGuard نصب کن
2️⃣ کانفیگ رو ایمپورت کن
3️⃣ اتصال رو بزن
"""

    await update.message.reply_text(text)


# ===== پشتیبانی =====
async def support(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(
        f"🛠 برای پشتیبانی به ادمین پیام بده:\n\nID: {ADMIN_ID}"
    )


# ===== هندل پیام =====
async def menu_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):

    text = update.message.text

    if text == "📦 اشتراک های من":
        await my_subscription(update, context)

    elif text == "💳 خرید اشتراک":
        await buy_subscription(update, context)

    elif text == "🏆 امتیاز های من":
        await my_points(update, context)

    elif text == "📚 آموزش ربات":
        await tutorial(update, context)

    elif text == "🛠 پشتیبانی":
        await support(update, context)


# ===== اجرای ربات =====
app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("config", send_config))

app.add_handler(MessageHandler(filters.TEXT, menu_handler))

app.run_polling()
