from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


def register_buy_handlers(bot):

    @bot.message_handler(func=lambda m: m.text == "🛒 خرید اشتراک")
    def buy_subscription(message):

        markup = InlineKeyboardMarkup()

        markup.add(
            InlineKeyboardButton("اشتراک 1 ماهه", callback_data="sub_1"),
            InlineKeyboardButton("اشتراک 3 ماهه", callback_data="sub_3"),
            InlineKeyboardButton("اشتراک 6 ماهه", callback_data="sub_6")
        )

        bot.send_message(
            message.chat.id,
            "📦 یکی از پلن ها را انتخاب کن:",
            reply_markup=markup
        )


    # انتخاب پلن
    @bot.callback_query_handler(func=lambda call: call.data.startswith("sub_"))
    def choose_plan(call):

        if call.data == "sub_1":
            price = "100 هزار تومان"

        elif call.data == "sub_3":
            price = "250 هزار تومان"

        elif call.data == "sub_6":
            price = "400 هزار تومان"

        bot.answer_callback_query(call.id)

        bot.send_message(
            call.message.chat.id,
            f"💰 قیمت پلن انتخابی:\n{price}\n\nبرای پرداخت با ادمین تماس بگیر."
        )
