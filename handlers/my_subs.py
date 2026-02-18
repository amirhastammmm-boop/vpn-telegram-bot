from telebot import types
from database import get_user_subscriptions, get_subscription
from utils import create_wireguard_conf


def register_my_sub_handlers(bot):

    @bot.message_handler(func=lambda m: m.text == "📦 اشتراک های من")
    def my_subscriptions(message):

        subs = get_user_subscriptions(message.from_user.id)

        if not subs:
            bot.send_message(message.chat.id, "❌ شما هیچ اشتراکی ندارید")
            return

        for sub in subs:

            text = f"""
🎗 شماره اشتراک: {sub[0]}

📅 تاریخ خرید: {sub[2]}
⏳ تاریخ اتمام: {sub[3]}
📊 حجم باقی مانده: {sub[4]}
"""

            markup = types.InlineKeyboardMarkup()

            markup.add(
                types.InlineKeyboardButton(
                    "📄 فایل شما",
                    callback_data=f"getfile_{sub[0]}"
                )
            )

            bot.send_message(message.chat.id, text, reply_markup=markup)

    @bot.callback_query_handler(func=lambda call: call.data.startswith("getfile_"))
    def send_config(call):

        sub_id = call.data.split("_")[1]

        sub = get_subscription(call.from_user.id, sub_id)

        if not sub:
            return

        file_path = create_wireguard_conf(call.from_user.id, sub)

        with open(file_path, "rb") as f:
            bot.send_document(call.message.chat.id, f)

        bot.answer_callback_query(call.id)
