from database import get_subs

def register_my_sub_handlers(bot):

    @bot.message_handler(func=lambda m: m.text == "📦 اشتراک های من")
    def my_subs(message):

        subs = get_subs(message.from_user.id)

        if not subs:
            bot.send_message(message.chat.id, "اشتراکی نداری ❌")
            return

        text = ""
        for s in subs:
            text += f"\n{ s[0] } ماهه\nاز { s[1] }\nتا { s[2] }\n"

        bot.send_message(message.chat.id, text)
