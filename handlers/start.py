from telebot import types

def register_start_handlers(bot):

    @bot.message_handler(commands=['start'])
    def start(message):

        args = message.text.split()

        if len(args) > 1:
            code = args[1]

            # ذخیره کد رفرال
            # save_referral(message.from_user.id, code)

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add("🛒 خرید اشتراک")
        markup.add("⭐ امتیازهای من")

        bot.send_message(
            message.chat.id,
            "به ربات فروش کانفیگ خوش اومدی 👋",
            reply_markup=markup
        )
