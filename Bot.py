from telegram import *
from telegram.ext import *
import config
import database
import payments


app = Application.builder().token(config.BOT_TOKEN).build()


# شروع ربات
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user = update.effective_user
    args = context.args

    inviter = None
    if args:
        inviter = int(args[0])

    database.add_user(user.id, inviter)

    keyboard = ReplyKeyboardMarkup([
        ["🛒 خرید اشتراک"],
        ["🏆 امتیاز های من"]
    ], resize_keyboard=True)

    await update.message.reply_text("به ربات خوش اومدی", reply_markup=keyboard)


# ================= خرید اشتراک =================

async def buy_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):

    keyboard = [[InlineKeyboardButton("ادامه خرید", callback_data="continue_buy")]]

    await update.message.reply_text(
        "منو خرید اشتراک:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


async def continue_buy(update: Update, context: ContextTypes.DEFAULT_TYPE):

    q = update.callback_query
    await q.answer()

    keyboard = [[InlineKeyboardButton("خرید با درگاه پرداخت مستقیم", callback_data="direct_pay")]]

    await q.edit_message_text(
        "⚠️ توجه داشته باشید هر باری که خرید میکنید یک اشتراک جدید دریافت میکنید\n\n"
        "✅برای ادامه دکمه زیر را فشار دهید",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


async def direct_pay(update: Update, context: ContextTypes.DEFAULT_TYPE):

    q = update.callback_query
    await q.answer()

    keyboard = [
        [InlineKeyboardButton("یک ماهه ۱۲۸ هزار", callback_data="pay_1")],
        [InlineKeyboardButton("دو ماهه ۱۹۸ هزار", callback_data="pay_2")],
        [InlineKeyboardButton("سه ماهه ۳۲۹ هزار", callback_data="pay_3")]
    ]

    await q.edit_message_text(
        "👈 لطفا یک گزینه را انتخاب کنید",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


async def create_pay(update: Update, context: ContextTypes.DEFAULT_TYPE):

    q = update.callback_query
    await q.answer()

    prices = {
        "pay_1": 128000,
        "pay_2": 198000,
        "pay_3": 329000
    }

    amount = prices[q.data]

    link = payments.create_payment(amount)

    await q.message.reply_text(f"لینک پرداخت:\n{link}")


# ================= امتیاز =================

async def points_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user = update.effective_user.id

    points = database.get_points(user)
    ref_count = database.get_ref_count(user)

    link = f"https://t.me/{config.BOT_USERNAME}?start={user}"

    text = f"""
🏆 با معرفی ربات امتیاز بگیر

🎖 امتیاز شما: {points}
🙍‍♂️ زیرمجموعه شما: {ref_count}

🌍 لینک اختصاصی شما:
{link}
"""

    await update.message.reply_text(text)


# ================= هندلر ها =================

app.add_handler(CommandHandler("start", start))

app.add_handler(MessageHandler(filters.TEXT == "🛒 خرید اشتراک", buy_menu))
app.add_handler(MessageHandler(filters.TEXT == "🏆 امتیاز های من", points_menu))

app.add_handler(CallbackQueryHandler(continue_buy, pattern="continue_buy"))
app.add_handler(CallbackQueryHandler(direct_pay, pattern="direct_pay"))
app.add_handler(CallbackQueryHandler(create_pay, pattern="pay_"))


print("Bot Running...")
app.run_polling()
