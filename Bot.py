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
    btn6 = KeyboardButton("🏠 منو")

    markup.row(btn1, btn2)
    markup.row(btn3, btn4)
    markup.row(btn5)
    markup.row(btn6)

    return markup


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(
        message.chat.id,
        "سلام 👋\nبه ربات VPN خوش اومدی",
        reply_markup=main_menu()
    )


@bot.message_handler(func=lambda m: True)
def buttons(message):

    if message.text == "💳 خرید اشتراک":
        bot.send_message(message.chat.id, "بخش خرید اشتراک", reply_markup=main_menu())

    elif message.text == "📦 اشتراک های من":
        bot.send_message(message.chat.id, "لیست اشتراک های شما", reply_markup=main_menu())

    elif message.text == "📚 آموزش":
        bot.send_message(message.chat.id, "آموزش استفاده", reply_markup=main_menu())

    elif message.text == "⭐ امتیاز":
        bot.send_message(message.chat.id, "امتیاز بده ❤️", reply_markup=main_menu())

    elif message.text == "📞 پشتیبانی":
        bot.send_message(message.chat.id, "ارتباط با پشتیبانی", reply_markup=main_menu())

    elif message.text == "🏠 منو":
        bot.send_message(message.chat.id, "بازگشت به منو", reply_markup=main_menu())


print("Bot Started...")
bot.infinity_polling()
