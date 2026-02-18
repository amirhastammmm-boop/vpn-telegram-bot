from database import get_user_subscriptions


def register_my_sub_handlers(bot):

    @bot.message_handler(func=lambda m: m.text == "📦 اشتراک های من")
    def my_subs(message):

        subs = get_user_subscriptions(message.from_user.id)

        if not subs:
            bot.send_message(message.chat.id, "اشتراکی نداری")
            return

        text = "📦 اشتراک های شما:\n\n"

        for sub in subs:
            text += f"📅 شروع: {sub['start']}\n"
            text += f"⏳ پایان: {sub['end']}\n"
            text += f"📦 مدت: {sub['months']} ماه\n"
            text += "-----------------\n"

        bot.send_message(message.chat.id, text)
