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
با خرید اشتراک توسط زیرمجموعه = امتیاز

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


    @bot.callback_query_handler(func=lambda c: c.data.startswith("buy_"))
    def buy_with_points(call):

        user_id = call.from_user.id
        points = get_user_points(user_id)

        need = 5 if call.data == "buy_5" else 9
        months = 1 if need == 5 else 2

        if points < need:
            bot.answer_callback_query(call.id, "❌ امتیاز کافی نیست")
            return

        bot.send_message(call.message.chat.id, f"✅ اشتراک {months} ماهه ساخته شد")
