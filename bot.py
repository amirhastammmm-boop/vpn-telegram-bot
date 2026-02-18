import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton

from config import BOT_TOKEN
from database import create_tables, add_user
from handlers import register_handlers


# ---------- ساخت ربات ----------
bot = telebot.TeleBot(BOT_TOKEN)


# ---------- ساخت دیتابیس ----------
create_tables()


# ---------- منوی اصلی ----------
def main_menu():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)

    markup.row(
        KeyboardButton("💳 خرید اشتراک"),
        KeyboardButton("📦 اشتراک های من")
    )

    markup.row(
        KeyboardButton("🏆 امتیاز من"),
        KeyboardButton("📚 آموزش خرید")
    )

    markup.row(
        KeyboardButton("🛠 پشتیبانی")
    )

    return markup


# ---------- استارت ----------
@bot.message_handler(commands=['start'])
def start(message):

    user_id = message.from_user.id

    # ثبت کاربر در دیتابیس
    add_user(user_id)

    text = """
❤️ سلام دوست عزیز

به ربات فروش VPN خوش آمدید

👇 یکی از گزینه های زیر را انتخاب کنید
"""

    bot.send_message(
        message.chat.id,
        text,
        reply_markup=main_menu()
    )


# ---------- ثبت سایر منوها ----------
register_handlers(bot)


# ---------- اجرای ربات ----------
print("Bot is running...")
bot.infinity_polling()
