import telebot
from config import BOT_TOKEN
from database import create_tables, add_subscription
from handlers import register_handlers
from telebot.types import ReplyKeyboardMarkup
from datetime import datetime, timedelta


bot = telebot.TeleBot(BOT_TOKEN)

# ساخت دیتابیس
create_tables()


# ---------------- منوی اصلی ----------------
def main_menu():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)

    markup.row("💳 خرید اشتراک", "📦 اشتراک های من")
    markup.row("🏆 امتیاز های من", "📚 آموزش خرید")
    markup.row("🛠 پشتیبانی")

    return markup


# ---------------- استارت ----------------
@bot.message_handler(commands=['start'])
def start(message):

    text = """
♥️ سلام دوست عزیز

به ربات پینگ خور خوش اومدی

⬇️ لطفا یک گزینه را انتخاب کن
"""

    bot.send_message(
        message.chat.id,
        text,
        reply_markup=main_menu()
    )


# ---------------- تست ساخت اشتراک ----------------
@bot.message_handler(commands=['testsub'])
def test_sub(message):

    user_id = message.from_user.id

    buy_date = datetime.now().strftime("%Y-%m-%d")
    expire_date = (datetime.now() + timedelta(days=30)).strftime("%Y-%m-%d")

    data = (
        user_id,
        buy_date,
        expire_date,
        "36GB",
        "TEST_PRIVATE_KEY",
        "10.0.0.2/32",
        "TEST_SERVER_KEY",
        "1.1.1.1:51820"
    )

    add_subscription(data)

    bot.send_message(message.chat.id, "✅ اشتراک تستی ساخته شد")


# ثبت هندلرها
register_handlers(bot)


print("Bot is running...")
bot.infinity_polling()
