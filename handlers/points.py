from database import get_user

def register_points_handlers(bot):

    @bot.message_handler(func=lambda m: m.text == "🏆 امتیاز های من")
    def points(message):

        user = get_user(message.from_user.id)

        if not user:
            bot.send_message(message.chat.id, "خطا ❌")
            return

        pts = user[3]

        bot.send_message(
            message.chat.id,
            f"🏆 امتیاز شما: {pts}\n\n"
            "5 امتیاز = 1 ماه\n"
            "9 امتیاز = 2 ماه"
        )
