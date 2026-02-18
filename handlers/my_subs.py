from database import get_subs

def register_my_sub_handlers(bot):

    @bot.message_handler(func=lambda m: m.text == "📦 اشتراک های من")
    def my_subs(message):

        subs = get_subs(message.from_user.id)

        if not subs:
            bot.send_message(message.chat.id, "❌ اشتراکی نداری")
            return

        text = "📦 اشتراک های شما:\n\n"

        for s in subs:
            months, start, end, config = s
            text += (
                f"{months} ماهه\n"
                f"شروع: {start[:10]}\n"
                f"پایان: {end[:10]}\n\n"
            )

        bot.send_message(message.chat.id, text)
