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

from config import TOKEN, PAYMENT_LINKS


# ---------- منوی اصلی ----------

def main_menu():

    keyboard = [
        [KeyboardButton("💳 خرید اشتراک"), KeyboardButton("📦 اشتراک های من")],
        [KeyboardButton("🏆 امتیاز های من"), KeyboardButton("📚 آموزش ربات")],
        [KeyboardButton("🛠 پشتیبانی")]
    ]

    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)


# ---------- استارت ----------

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    text = """
♥️سلام دوست عزیز

به ربات پینگ خور خوش اومدی

⬇️لطفا یک گزینه رو انتخاب کن
"""

    await update.message.reply_text(text, reply_markup=main_menu())


# ---------- خرید اشتراک ----------

async def buy_subscription(update: Update, context: ContextTypes.DEFAULT_TYPE):

    text = """
⚠️ توجه داشته باشید هر باری که خرید میکنید یک اشتراک جدید با فایل های جدید دریافت میکنید و اشتراک هایی که قبلا تمام شده اند تمدید نمیشوند و باید از فایل های اشتراک جدید استفاده کنید


✅برای ادامه دکمه زیر را فشار دهید
"""

    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("➡️ ادامه خرید", callback_data="continue_buy")]
    ])

    await update.message.reply_text(text, reply_markup=keyboard)


# ---------- ادامه خرید ----------

async def continue_buy(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    await query.answer()

    text = "👈لطفا یک گزینه را انتخاب کنید"

    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("💳 خرید با درگاه پرداخت مستقیم", callback_data="direct_payment")]
    ])

    await query.message.reply_text(text, reply_markup=keyboard)


# ---------- پلن ها ----------

async def direct_payment(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    await query.answer()

    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("🟢 یک کاربره یک ماهه 36GB — 128هزار", url=PAYMENT_LINKS["sub1"])],
        [InlineKeyboardButton("🟡 یک کاربره دو ماهه 78GB — 198هزار", url=PAYMENT_LINKS["sub2"])],
        [InlineKeyboardButton("🔵 یک کاربره سه ماهه 127GB — 329هزار", url=PAYMENT_LINKS["sub3"])]
    ])

    await query.message.reply_text(
        "💰 لطفا پلن مورد نظر را انتخاب کنید",
        reply_markup=keyboard
    )


# ---------- اشتراک های من ----------

async def my_subscriptions(update: Update, context: ContextTypes.DEFAULT_TYPE):

    text = """
🎗شماره اشتراک: 2135081
🎯نوع اشتراک: یک ماهه
⏰تاریخ خرید: 2026-02-09 20:23:19
حجم مجاز: 37888 مگابایت
حجم مصرف شده: 9946 مگابایت
⚙️وضعیت: ✅فعال

(اطلاعات هر 4 ساعت یکبار بروزرسانی میشود)
"""

    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("📥 دریافت مجدد کانفیگ", callback_data="get_config")]
    ])

    await update.message.reply_text(text, reply_markup=keyboard)


# ---------- ارسال کانفیگ تست ----------

async def send_config(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    await query.answer()

    config_text = """
[Interface]
PrivateKey = TEST_KEY
Address = 10.0.0.2/24
DNS = 1.1.1.1
"""

    with open("vpn.conf", "w") as f:
        f.write(config_text)

    await query.message.reply_document(document=open("vpn.conf", "rb"))


# ---------- امتیاز ----------

async def points(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_id = update.message.from_user.id

    ref_link = f"https://t.me/PayydarVpn_robot?start={user_id}"

    text = f"""
🏆 امتیاز شما: 0

🔗 لینک دعوت شما:
{ref_link}

هر 5 دعوت = اشتراک 1 ماهه
هر 8 دعوت = اشتراک 2 ماهه
"""

    await update.message.reply_text(text)


# ---------- آموزش ----------

async def tutorial(update: Update, context: ContextTypes.DEFAULT_TYPE):

    text = """
📚 آموزش استفاده از Wireguard

1️⃣ برنامه Wireguard را نصب کنید
2️⃣ فایل کانفیگ را ایمپورت کنید
3️⃣ اتصال را فعال کنید
"""

    await update.message.reply_text(text)


# ---------- پشتیبانی ----------

async def support(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(
        "جهت پشتیبانی به آیدی زیر پیام دهید:\n@633464148"
    )


# ---------- هندل پیام ----------

async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):

    text = update.message.text

    if text == "💳 خرید اشتراک":
        await buy_subscription(update, context)

    elif text == "📦 اشتراک های من":
        await my_subscriptions(update, context)

    elif text == "🏆 امتیاز های من":
        await points(update, context)

    elif text == "📚 آموزش ربات":
        await tutorial(update, context)

    elif text == "🛠 پشتیبانی":
        await support(update, context)


# ---------- اجرای ربات ----------

def main():

    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))

    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message_handler))

    app.add_handler(CallbackQueryHandler(continue_buy, pattern="continue_buy"))
    app.add_handler(CallbackQueryHandler(direct_payment, pattern="direct_payment"))
    app.add_handler(CallbackQueryHandler(send_config, pattern="get_config"))

    print("Bot Started...")
    app.run_polling()


if __name__ == "__main__":
    main()
