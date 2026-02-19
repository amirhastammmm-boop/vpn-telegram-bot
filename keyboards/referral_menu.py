from telegram import InlineKeyboardMarkup, InlineKeyboardButton

def referral_menu():
    keyboard = [
        [InlineKeyboardButton("دریافت اشتراک با امتیاز", callback_data="redeem")]
    ]
    return InlineKeyboardMarkup(keyboard)
