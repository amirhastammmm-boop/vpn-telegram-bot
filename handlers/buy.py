from telebot.types import Message


def register_buy_handlers(bot):

    @bot.message_handler(func=lambda message: message.text == "🛒 خرید اکانت")
    def buy_account(message: Message):
        bot.send_message(message.chat.id, "بخش خرید اکانت به زودی اضافه میشه 🚀")
