from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from database import create_subscription


def register_buy_handlers(bot):

    @bot.message_handler(func=lambda m: m.text == "🛒 خرید اشتراک")
    def buy_menu(message):

        kb = InlineKeyboardMarkup()
        kb.add(
            InlineKeyboardButton("یک ماهه", callback_data="buy_1"),
            InlineKeyboardButton("دو ماهه", callback_data="buy_2"),
            InlineKeyboardButton("سه ماهه", callback_data="buy_3"),
        )

        bot.send_message(
            message.chat.id,
            "پلن مورد نظر را انتخاب کن:",
            reply_markup=kb
        )

    @bot.callback_query_handler(func=lambda c: c.data.startswith("buy_"))
    def buy_callback(call):

        user_id = call.from_user.id
        plan = call.data.split("_")[1]

        months = int(plan)

        create_subscription(user_id, months)

        bot.answer_callback_query(call.id)
        bot.send_message(
            call.message.chat.id,
            "✅ اشتراک با موفقیت ثبت شد\n"
            "فعلا پرداخت تستی است"
        )
