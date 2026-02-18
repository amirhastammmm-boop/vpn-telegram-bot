from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from database import add_user, get_user


def register_start_handler(bot):

    @bot.message_handler(commands=['start'])
    def start(message):

        user_id = message.from_user.id
        first_name = message.from_user.first_name

        args = message.text.split()

        # اگر کاربر قبلا ثبت نشده بود
        if not get_user(user_id):

            # اگر با کد رفرال وارد شده
            if len(args) > 1:
                referral_code = args[1]
                add_user(user_id, referral_code)

            else:
                add_user(user_id)

        # ---------- منوی اصلی ----------
        markup = InlineKeyboardMarkup(row_width=2)

        markup.add(
            InlineKeyboardButton("👤 حساب کاربری", callback_data="profile"),
            InlineKeyboardButton("🎁 دعوت دوستان", callback_data="referral")
        )

        bot.send_message(
            message.chat.id,
            f"سلام {first_name} 👋\nبه ربات خوش اومدی ❤️",
            reply_markup=markup
        )
