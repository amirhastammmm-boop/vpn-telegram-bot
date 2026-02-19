import logging
import uuid
from datetime import datetime, timedelta

from telegram import (
    Update,
    ReplyKeyboardMarkup,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    InputFile,
)
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ContextTypes,
    filters,
)

TOKEN = "8443993110:AAH08NXvjcKty2XBHH13ecD8l5giSCD-ZF4"

logging.basicConfig(level=logging.INFO)

users = {}

# ------------------ MAIN MENU ------------------

def main_menu():
    keyboard = [
        ["خرید اشتراک", "اشتراک‌های من"],
        ["امتیازهای من", "آموزش"],
        ["پشتیبانی"],
    ]
    return ReplyKeyboardMarkup(
        keyboard, resize_keyboard=True, one_time_keyboard=False
    )

# ------------------ START ------------------

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    if user_id not in users:
        users[user_id] = {
            "subscriptions": [],
            "points": 0,
            "referral_code": str(user_id),
        }

    await update.message.reply_text(
        "به ربات خوش آمدید 👋",
        reply_markup=main_menu()
    )

# ------------------ BUY MENU ------------------

async def buy_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("۱ ماهه | ۳۳GB | 130k", callback_data="plan_1")],
        [InlineKeyboardButton("۲ ماهه | ۷۷GB | 260k", callback_data="plan_2")],
        [InlineKeyboardButton("۳ ماهه | ۱۱۰GB | 390k", callback_data="plan_3")],
    ]
    await update.message.reply_text(
        "یکی از پلن‌ها را انتخاب کنید:",
        reply_markup=InlineKeyboardMarkup(keyboard),
    )

# ------------------ CREATE SUB ------------------

def create_subscription(user_id, months, volume):
    sub_id = str(uuid.uuid4())[:8]
    start = datetime.now()
    end = start + timedelta(days=30 * months)

    subscription = {
        "id": sub_id,
        "months": months,
        "start": start,
        "end": end,
        "volume": volume,
        "remaining": volume,
    }

    users[user_id]["subscriptions"].append(subscription)
    return subscription

# ------------------ CALLBACK ------------------

async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    user_id = query.from_user.id

    plans = {
        "plan_1": (1, 33),
        "plan_2": (2, 77),
        "plan_3": (3, 110),
    }

    if query.data in plans:
        months, volume = plans[query.data]

        sub = create_subscription(user_id, months, volume)

        # فایل تستی به جای WireGuard
        config_text = f"""
TEST VPN CONFIG
Subscription ID: {sub['id']}
Start: {sub['start']}
End: {sub['end']}
Volume: {sub['volume']}GB
"""

        file_name = f"config_{sub['id']}.conf"
        with open(file_name, "w") as f:
            f.write(config_text)

        await query.message.reply_document(
            document=InputFile(file_name),
            caption="اشتراک تستی شما ساخته شد ✅"
        )

        await query.message.reply_text(
            "منوی اصلی 👇",
            reply_markup=main_menu()
        )

    elif query.data == "use_points":
        if users[user_id]["points"] >= 5:
            users[user_id]["points"] -= 5
            sub = create_subscription(user_id, 1, 33)

            await query.message.reply_text(
                "اشتراک رایگان با امتیاز ساخته شد ✅",
                reply_markup=main_menu()
            )
        else:
            await query.message.reply_text(
                "امتیاز کافی ندارید ❌",
                reply_markup=main_menu()
            )

# ------------------ MY SUBS ------------------

async def my_subs(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    subs = users[user_id]["subscriptions"]

    if not subs:
        await update.message.reply_text(
            "هیچ اشتراکی ندارید ❌",
            reply_markup=main_menu()
        )
        return

    text = ""
    for s in subs:
        days_left = (s["end"] - datetime.now()).days
        text += f"""
کد: {s['id']}
مدت: {s['months']} ماه
پایان: {s['end']}
روز باقی‌مانده: {days_left}
حجم کل: {s['volume']}GB
---------------------
"""

    await update.message.reply_text(text, reply_markup=main_menu())

# ------------------ POINTS ------------------

async def points(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user = users[user_id]

    keyboard = [
        [InlineKeyboardButton("دریافت اشتراک با امتیاز", callback_data="use_points")]
    ]

    text = f"""
کد رفرال شما:
{user['referral_code']}

امتیاز فعلی: {user['points']}

هر ۵ امتیاز = ۱ ماه رایگان
"""

    await update.message.reply_text(
        text,
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

# ------------------ TRAINING ------------------

async def training(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "آموزش استفاده:\n\n"
        "1- اپ WireGuard را نصب کنید.\n"
        "2- فایل کانفیگ را Import کنید.\n"
        "3- روی Connect بزنید.\n",
        reply_markup=main_menu()
    )

# ------------------ SUPPORT ------------------

async def support(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "در صورت بروز مشکل به پشتیبانی پیام دهید:\nAmnbytry@",
        reply_markup=main_menu()
    )

# ------------------ MESSAGE ROUTER ------------------

async def router(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    if text == "خرید اشتراک":
        await buy_menu(update, context)
    elif text == "اشتراک‌های من":
        await my_subs(update, context)
    elif text == "امتیازهای من":
        await points(update, context)
    elif text == "آموزش":
        await training(update, context)
    elif text == "پشتیبانی":
        await support(update, context)

# ------------------ MAIN ------------------

def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(handle_callback))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, router))

    print("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
