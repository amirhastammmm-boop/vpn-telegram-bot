from telegram import ReplyKeyboardMarkup

def main_menu():
    keyboard = [
        ["🛒 خرید اشتراک", "📦 اشتراک های من"],
        ["🏆 امتیاز های من", "📘 آموزش"],
        ["🛠 پشتیبانی"]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

def buy_menu():
    keyboard = [
        ["1 ماهه"],
        ["2 ماهه"],
        ["3 ماهه"],
        ["🔙 بازگشت"]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
