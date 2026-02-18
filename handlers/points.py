def register_points_handlers(bot):

    @bot.message_handler(func=lambda m: m.text == "⭐ امتیازات من")
    def my_points(message):
        bot.send_message(message.chat.id, "امتیاز شما: 0")
