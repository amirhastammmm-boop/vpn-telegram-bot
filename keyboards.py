from telebot.types import ReplyKeyboardMarkup, KeyboardButton


def main_menu():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)

    btn1 = KeyboardButton("🛒 خرید اشتراک")
    btn2 = KeyboardButton("📦 اشتراک های من")

    btn3 = KeyboardButton("🏆 امتیاز من")
    btn4 = KeyboardButton("📚 آموزش خرید")

    btn5 = KeyboardButton("🎧 پشتیبانی")

    markup.row(btn1, btn2)
    markup.row(btn3, btn4)
    markup.row(btn5)

    return markup
