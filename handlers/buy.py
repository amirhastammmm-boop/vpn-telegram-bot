from telebot import types

def register_buy_handlers(bot):

    @bot.message_handler(func=lambda m: m.text == "🛒 خرید اشتراک")
    def buy_menu(message):

        markup = types.InlineKeyboardMarkup()
        markup.add(
            types.InlineKeyboardButton(
                "خرید پلن 1 ماهه",
                callback_data="buy_1m"
            )
        )

        bot.send_message(
            message.chat.id,
            "پلن مورد نظر رو انتخاب کن:",
            reply_markup=markup
        )


    @bot.callback_query_handler(func=lambda c: c.data.startswith("buy_"))
    def create_invoice(call):

        user_id = call.from_user.id
        plan = call.data.split("_")[1]

        # ساخت فاکتور
        pay_link = create_payment(user_id, plan)

        bot.send_message(
            call.message.chat.id,
            f"برای پرداخت روی لینک بزن:\n{pay_link}"
        )
