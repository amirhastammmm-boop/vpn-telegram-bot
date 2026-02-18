import telebot
from config import BOT_TOKEN
from database import create_tables, add_user
from handlers import register_handlers
from telebot.types import ReplyKeyboardMarkup

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

    args = message.text.split()
    referral = args[1] if len(args) > 1 else None

    add_user(message.from_user.id)

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


# ثبت هندلرها
register_handlers(bot)


print("Bot is running...")
bot.infinity_polling()
