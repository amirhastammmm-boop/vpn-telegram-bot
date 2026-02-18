from database import get_user, add_points, create_subscription

def register_points_handlers(bot):

    @bot.message_handler(func=lambda m: m.text == "🏆 امتیاز های من")
    def points(message):

        user = get_user(message.from_user.id)
        pts = user[3]

        bot.send_message(
            message.chat.id,
            f"امتیاز شما: {pts}\n\n5 امتیاز = 1 ماه\n9 امتیاز = 2 ماه"
        )
