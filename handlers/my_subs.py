def register_my_sub_handlers(bot):

    @bot.message_handler(func=lambda m: m.text == "⭐ امتیازهای من")
    def my_points(message):

        pts = get_points(message.from_user.id)

        bot.send_message(
            message.chat.id,
            f"امتیاز شما: {pts}"
        )
