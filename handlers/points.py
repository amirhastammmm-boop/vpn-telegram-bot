from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from database import get_user_points


def register_points_handlers(bot):

    @bot.message_handler(func=lambda m: m.text == "🏆 امتیاز های من")
    def show_points(message):

        user_id = message.from_user.id
        points = get_user_points(user_id)

        text = f"""
🏆 امتیاز شما: {points}

📌 قوانین:

با دعوت هر نفر = 1 امتیاز

🎁 جوایز:
5 امتیاز = اشتراک 1 ماهه
9 امتیاز = اشتراک 2 ماهه
"""

        keyboard = InlineKeyboardMarkup()

        keyboard.add(
            InlineKeyboardButton("🎁 خرید با 5 امتیاز", callback_data="buy_5"),
            InlineKeyboardButton("🎁 خرید با 9 امتیاز", callback_data="buy_9")
        )

        bot.send_message(message.chat.id, text, reply_markup=keyboard)
