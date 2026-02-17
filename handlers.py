from keyboards import main_menu


def register_handlers(bot):

    @bot.message_handler(commands=['start'])
    def start(message):
        text = """
👋 به ربات فروش VPN خوش آمدید

لطفاً از منوی زیر گزینه مورد نظر خود را انتخاب کنید
"""
        bot.send_message(message.chat.id, text, reply_markup=main_menu())

    @bot.message_handler(func=lambda m: m.text == "🛒 خرید اشتراک")
    def buy_subscription(message):
        bot.send_message(message.chat.id, "🛒 وارد منوی خرید اشتراک شدید", reply_markup=main_menu())

    @bot.message_handler(func=lambda m: m.text == "📦 اشتراک های من")
    def my_sub(message):
        bot.send_message(message.chat.id, "📦 لیست اشتراک های شما", reply_markup=main_menu())

    @bot.message_handler(func=lambda m: m.text == "🏆 امتیاز من")
    def points(message):
        bot.send_message(message.chat.id, "🏆 امتیاز های شما", reply_markup=main_menu())

    @bot.message_handler(func=lambda m: m.text == "📚 آموزش خرید")
    def tutorial(message):
        bot.send_message(message.chat.id, "📚 آموزش خرید اشتراک", reply_markup=main_menu())

    @bot.message_handler(func=lambda m: m.text == "🎧 پشتیبانی")
    def support(message):
        bot.send_message(message.chat.id, "🎧 ارتباط با پشتیبانی", reply_markup=main_menu())
