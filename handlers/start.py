from telebot.types import ReplyKeyboardMarkup, KeyboardButton


def register_start_handler(bot):

    @bot.message_handler(commands=["start"])
    def start(message):

        markup = ReplyKeyboardMarkup(resize_keyboard=True)

        markup.add(
            KeyboardButton("🛒 خرید اشتراک"),
            KeyboardButton("📦 اشتراک من"),
            KeyboardButton("⭐ امتیازات من")
        )

        bot.send_message(
            message.chat.id,
            "به ربات خوش اومدی 🌹",
            reply_markup=markup
        )
