from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


def register_buy_handlers(bot):

    @bot.message_handler(func=lambda m: m.text == "🛒 خرید اشتراک")
    def buy_menu(message):

        markup = InlineKeyboardMarkup(row_width=1)

        markup.add(
            InlineKeyboardButton("اشتراک 1 ماهه", callback_data="buy_1"),
            InlineKeyboardButton("اشتراک 3 ماهه", callback_data="buy_3")
        )

        bot.send_message(
            message.chat.id,
            "📦 یکی از اشتراک ها را انتخاب کن:",
            reply_markup=markup
        )


    @bot.callback_query_handler(func=lambda c: c.data.startswith("buy_"))
    def buy_callback(call):

        if call.data == "buy_1":
            text = "💰 قیمت اشتراک 1 ماهه: ..."
        else:
            text = "💰 قیمت اشتراک 3 ماهه: ..."

        bot.send_message(call.message.chat.id, text)
