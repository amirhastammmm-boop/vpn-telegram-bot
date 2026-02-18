from telebot.types import ReplyKeyboardMarkup, KeyboardButton
from database import add_user


def main_menu():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)

    kb.add(KeyboardButton("🛒 خرید اشتراک"))
    kb.add(KeyboardButton("📦 اشتراک های من"))
    kb.add(KeyboardButton("🏆 امتیاز های من"))

    return kb


def register_start_handlers(bot):

    @bot.message_handler(commands=['start'])
    def start(message):

        user_id = message.from_user.id
        add_user(user_id)

        bot.send_message(
            message.chat.id,
            "❤️ سلام دوست عزیز\n"
            "به ربات خوش اومدی\n\n"
            "لطفا یک گزینه را انتخاب کن 👇",
            reply_markup=main_menu()
        )
