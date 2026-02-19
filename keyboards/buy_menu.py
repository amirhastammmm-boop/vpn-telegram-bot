from telegram import InlineKeyboardMarkup, InlineKeyboardButton

def buy_menu():
    keyboard = [
        [InlineKeyboardButton("اشتراک ۱ ماهه | ۳۳ گیگ | ۱۳۰,۰۰۰ تومان", callback_data="plan_1")],
        [InlineKeyboardButton("اشتراک ۲ ماهه | ۷۷ گیگ | ۲۶۰,۰۰۰ تومان", callback_data="plan_2")],
        [InlineKeyboardButton("اشتراک ۳ ماهه | ۱۱۰ گیگ | ۳۹۰,۰۰۰ تومان", callback_data="plan_3")]
    ]
    return InlineKeyboardMarkup(keyboard)
