from telebot import types
from database import create_subscription, add_points, get_user

def register_buy_handlers(bot):

    @bot.message_handler(func=lambda m: m.text == "💳 خرید اشتراک")
    def buy(message):

        markup = types.InlineKeyboardMarkup()
        markup.add(
            types.InlineKeyboardButton("1 ماهه", callback_data="buy_1"),
            types.InlineKeyboardButton("2 ماهه", callback_data="buy_2"),
            types.InlineKeyboardButton("3 ماهه", callback_data="buy_3")
        )

        bot.send_message(message.chat.id, "پلن رو انتخاب کن:", reply_markup=markup)

    @bot.callback_query_handler(func=lambda c: c.data.startswith("buy_"))
    def fake_payment(call):

        months = int(call.data.split("_")[1])
        user_id = call.from_user.id

        # شبیه سازی پرداخت موفق
        create_subscription(user_id, months)

        user = get_user(user_id)
        invited_by = user[2]

        if invited_by:
            add_points(invited_by, months)

        bot.send_message(call.message.chat.id, "✅ پرداخت موفق بود (فیک)")
