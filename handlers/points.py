from database import get_user_points, use_points, create_subscription


def register_points_handlers(bot):

    @bot.message_handler(func=lambda m: m.text == "🏆 امتیاز های من")
    def points_menu(message):

        points = get_user_points(message.from_user.id)

        bot.send_message(
            message.chat.id,
            f"🏆 امتیاز شما: {points}\n\n"
            "۵ امتیاز = اشتراک ۱ ماهه\n"
            "۹ امتیاز = اشتراک ۲ ماهه"
        )

    @bot.message_handler(func=lambda m: m.text == "خرید با ۵ امتیاز")
    def buy_with_5(message):

        if use_points(message.from_user.id, 5):
            create_subscription(message.from_user.id, 1)
            bot.send_message(message.chat.id, "اشتراک ۱ ماهه فعال شد")
        else:
            bot.send_message(message.chat.id, "امتیاز کافی نیست")

    @bot.message_handler(func=lambda m: m.text == "خرید با ۹ امتیاز")
    def buy_with_9(message):

        if use_points(message.from_user.id, 9):
            create_subscription(message.from_user.id, 2)
            bot.send_message(message.chat.id, "اشتراک ۲ ماهه فعال شد")
        else:
            bot.send_message(message.chat.id, "امتیاز کافی نیست")
