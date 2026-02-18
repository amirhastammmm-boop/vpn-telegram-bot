from telebot import types
from database import add_user

def register_start_handlers(bot):

    @bot.message_handler(commands=['start'])
    def start(message):

        args = message.text.split()
        ref_code = args[1] if len(args) > 1 else None

        add_user(message.from_user.id, ref_code)

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.row("💳 خرید اشتراک", "📦 اشتراک های من")
        markup.row("🏆 امتیاز های من")

        bot.send_message(
            message.chat.id,
            "سلام دوست عزیز ❤️\nبه ربات خوش اومدی",
            reply_markup=markup
        )
