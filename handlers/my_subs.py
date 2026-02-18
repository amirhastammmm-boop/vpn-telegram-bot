from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from database import get_user_subscriptions


def register_my_sub_handlers(bot):

    @bot.message_handler(func=lambda m: m.text == "📦 اشتراک های من")
    def show_my_subs(message):

        user_id = message.from_user.id
        subs = get_user_subscriptions(user_id)

        if not subs:
            bot.send_message(message.chat.id, "❌ شما هنوز اشتراکی ندارید")
            return

        for sub in subs:

            sub_id = sub[0]
            buy_date = sub[2]
            expire_date = sub[3]
            volume = sub[4]

            text = f"""
📦 اشتراک شما

📅 تاریخ خرید: {buy_date}
⏳ تاریخ انقضا: {expire_date}
📊 حجم: {volume}
"""

            keyboard = InlineKeyboardMarkup()
            keyboard.add(
                InlineKeyboardButton(
                    "📄 فایل شما",
                    callback_data=f"file_{sub_id}"
                )
            )

            bot.send_message(message.chat.id, text, reply_markup=keyboard)


    @bot.callback_query_handler(func=lambda call: call.data.startswith("file_"))
    def send_file(call):

        bot.answer_callback_query(call.id)

        bot.send_message(call.message.chat.id, "ساخت فایل هنوز اضافه نشده")
