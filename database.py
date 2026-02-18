from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from database import add_user, get_user, add_points, get_user_points


def register_start_handler(bot):

    # ---------- استارت ----------
    @bot.message_handler(commands=['start'])
    def start(message):

        user_id = message.from_user.id
        first_name = message.from_user.first_name
        args = message.text.split()

        # اگر کاربر قبلا ثبت نشده بود
        if not get_user(user_id):

            # اگر با رفرال وارد شده
            if len(args) > 1:
                try:
                    referrer_id = int(args[1])

                    if referrer_id != user_id:
                        add_user(user_id, referrer_id)
                        add_points(referrer_id, 5)

                        bot.send_message(
                            referrer_id,
                            "🎉 یک نفر با لینک شما عضو شد!\n➕ 5 امتیاز گرفتی"
                        )
                    else:
                        add_user(user_id)

                except:
                    add_user(user_id)

            else:
                add_user(user_id)

        send_main_menu(message.chat.id, first_name)


    # ---------- منوی اصلی ----------
    def send_main_menu(chat_id, name):

        markup = InlineKeyboardMarkup(row_width=2)

        markup.add(
            InlineKeyboardButton("👤 حساب کاربری", callback_data="profile"),
            InlineKeyboardButton("🎁 دعوت دوستان", callback_data="referral")
        )

        bot.send_message(
            chat_id,
            f"سلام {name} 👋\nبه ربات خوش اومدی ❤️",
            reply_markup=markup
        )


    # ---------- پروفایل ----------
    @bot.callback_query_handler(func=lambda c: c.data == "profile")
    def profile(call):

        user_id = call.from_user.id
        points = get_user_points(user_id)

        text = f"""
👤 پروفایل شما

🆔 آیدی عددی: {user_id}
🏆 امتیاز: {points}
"""

        bot.answer_callback_query(call.id)
        bot.send_message(call.message.chat.id, text)


    # ---------- دعوت دوستان ----------
    @bot.callback_query_handler(func=lambda c: c.data == "referral")
    def referral(call):

        user_id = call.from_user.id
        bot_username = bot.get_me().username

        link = f"https://t.me/{bot_username}?start={user_id}"

        text = f"""
🎁 لینک دعوت شما:

{link}

با دعوت هر نفر 5 امتیاز میگیری ✅
"""

        bot.answer_callback_query(call.id)
        bot.send_message(call.message.chat.id, text)
