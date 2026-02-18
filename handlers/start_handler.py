from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from database import get_user, add_user, add_points


def register_start_handler(bot):

    @bot.message_handler(commands=['start'])
    def start(message):

        user_id = message.from_user.id
        first_name = message.from_user.first_name

        # بررسی وجود کاربر
        if not get_user(user_id):
            add_user(user_id)

            # بررسی رفرال
            args = message.text.split()

            if len(args) > 1:
                try:
                    referrer_id = int(args[1])

                    if referrer_id != user_id and get_user(referrer_id):
                        add_points(referrer_id, 5)

                        bot.send_message(
                            referrer_id,
                            "🎉 یک نفر با لینک رفرال شما عضو شد!\n"
                            "➕ 5 امتیاز دریافت کردی"
                        )
                except:
                    pass

        # منوی اصلی
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
```0
