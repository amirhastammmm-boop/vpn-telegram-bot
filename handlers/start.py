from telebot import types
from database import create_user

def register_start_handlers(bot):

    @bot.message_handler(commands=['start'])
    def start(message):
        args = message.text.split()
        invited_by = None

        if len(args) > 1:
            try:
                invited_by = int(args[1])
            except:
                invited_by = None

        create_user(message.from_user.id, invited_by)

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add("💳 خرید اشتراک")
        markup.add("📦 اشتراک های من")
        markup.add("🏆 امتیاز های من")

        bot.send_message(
            message.chat.id,
            "خوش اومدی 👋",
            reply_markup=markup
        )
