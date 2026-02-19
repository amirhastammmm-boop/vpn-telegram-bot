from telegram import ReplyKeyboardMarkup

def main_menu():
    keyboard = [
        ["خرید اشتراک", "اشتراک‌های من"],
        ["امتیازهای من", "آموزش"],
        ["پشتیبانی"]
    ]

    return ReplyKeyboardMarkup(
        keyboard,
        resize_keyboard=True,
        one_time_keyboard=False
    )
