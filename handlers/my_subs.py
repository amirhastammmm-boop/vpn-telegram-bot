def register_my_sub_handlers(bot):

    @bot.message_handler(func=lambda m: m.text == "📦 اشتراک من")
    def my_sub(message):
        bot.send_message(message.chat.id, "شما فعلاً اشتراک فعالی ندارید.")
