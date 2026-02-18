from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from database import add_user


def register_start_handlers(bot):

    @bot.message_handler(commands=['ref'])
    def referral_panel(message):

        user_id = message.from_user.id

        referral_link = f"https://t.me/{bot.get_me().username}?start={user_id}"

        text = f"""
🎁 لینک دعوت شما:

{referral_link}

📌 با دعوت هر نفر 1 امتیاز میگیری
"""

        keyboard = InlineKeyboardMarkup()

        keyboard.add(
            InlineKeyboardButton("📤 اشتراک گذاری لینک", url=f"https://t.me/share/url?url={referral_link}")
        )

        bot.send_message(message.chat.id, text, reply_markup=keyboard)
