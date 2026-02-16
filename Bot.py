import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
import config

bot = telebot.TeleBot(config.BOT_TOKEN)


# ساخت منو
def main_menu():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)

    btn1 = KeyboardButton("💳 خرید اشتراک")
    btn2 = KeyboardButton("📦 اشتراک های من")
    btn3 = KeyboardButton("📚 آموزش")
    btn4 = KeyboardButton("⭐ امتیاز")
    btn5 = KeyboardButton("📞 پشتیبانی")

    markup.row(btn1, btn2)
    markup.row(btn3, btn4)
    markup.row(btn5)

    return markup


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(
        message.chat.id,
        "سلام 👋\nبه ربات VPN خوش اومدی",
        reply_markup=main_menu()
    )


# دکمه ها
@bot.message_handler(func=lambda m: True)
def buttons(message):

    if message.text == "💳 خرید اشتراک":
        bot.send_message(message.chat.id, "بخش خرید اشتراک")

    elif message.text == "📦 اشتراک های من":
        bot.send_message(message.chat.id, "لیست اشتراک های شما")

    elif message.text == "📚 آموزش":
        bot.send_message(message.chat.id, "آموزش استفاده")

    elif message.text == "⭐ امتیاز":
        bot.send_message(message.chat.id, "امتیاز بده ❤️")

    elif message.text == "📞 پشتیبانی":
        bot.send_message(message.chat.id, "ارتباط با پشتیبانی")


print("Bot Started...")
bot.infinity_polling()
