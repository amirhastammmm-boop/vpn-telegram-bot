from telegram import (
    Update,
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton
)

from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ContextTypes,
    filters
)

from config import TOKEN, ADMIN_ID

from database import (
    add_user,
    get_user_subscriptions,
    get_subscription_by_id,
    add_test_subscription
)


# ---------------- منوی اصلی ----------------

def main_menu():

    keyboard = [
        [KeyboardButton("💳 خرید اشتراک"), KeyboardButton("📦 اشتراک های من")],
        [KeyboardButton("🏆 امتیاز های من"), KeyboardButton("📚 آموزش ربات")],
        [KeyboardButton("🛠 پشتیبانی")]
    ]

    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)


# ---------------- استارت ----------------

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_id = update.message.from_user.id

    add_user(user_id)

    if not get_user_subscriptions(user_id):
        add_test_subscription(user_id)

    text = """
♥️سلام دوست عزیز

به ربات پینگ خور خوش اومدی

⬇️لطفا یک گزینه رو انتخاب کن
"""

    await update.message.reply_text(text, reply_markup=main_menu())


# ---------------- اشتراک های من ----------------

async def my_subscriptions(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_id = update.message.from_user.id
    subs = get_user_subscriptions(user_id)

    if not subs:
        await update.message.reply_text("❌ شما هیچ اشتراکی ندارید")
        return

    for sub in subs:

        sub_id = sub[0]
        sub_number = sub[2]
        sub_type = sub[3]
        buy_date = sub[4]
        total = sub[6]
        used = sub[7]
        status = sub[8]

        text = f"""
🎗شماره اشتراک: {sub_number}
🎯نوع اشتراک: {sub_type}
⏰تاریخ خرید: {buy_date}
حجم مجاز: {total} مگابایت
حجم مصرف شده: {used} مگابایت
⚙️وضعیت: {status}

(اطلاعات هر 4 ساعت یکبار بروزرسانی میشود)
"""

        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("📥 دریافت مجدد کانفیگ", callback_data=f"getconfig_{sub_id}")]
        ])

        await update.message.reply_text(text, reply_markup=keyboard)


# ---------------- ارسال کانفیگ ----------------

async def send_config(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    await query.answer()

    user_id = query.from_user.id
    sub_id = query.data.split("_")[1]

    sub = get_subscription_by_id(sub_id, user_id)

    if not sub:
        await query.message.reply_text("❌ اشتراک پیدا نشد")
        return

    config_text = sub[9]

    file_name = f"vpn_{sub_id}.conf"

    with open(file_name, "w") as f:
        f.write(config_text)

    await query.message.reply_document(document=open(file_name, "rb"))


# ---------------- اجرای ربات ----------------

def main():

    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))

    app.add_handler(MessageHandler(
        filters.TEXT & filters.Regex("📦 اشتراک های من"),
        my_subscriptions
    ))

    app.add_handler(CallbackQueryHandler(send_config, pattern="getconfig"))

    print("Bot is running...")
    app.run_polling()


if __name__ == "__main__":
    main()
