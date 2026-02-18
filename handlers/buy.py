from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import NEXT_PAY_LINKS


# ---------------- منو خرید اشتراک ----------------

def buy_menu(bot):

    @bot.message_handler(func=lambda m: m.text == "💳 خرید اشتراک")
    def buy_start(message):

        text = """
منو خرید اشتراک:

⚠️ توجه داشته باشید هر باری که خرید میکنید یک اشتراک جدید با فایل های جدید دریافت میکنید و اشتراک هایی که قبلا تمام شده اند تمدید نمیشوند و باید از فایل های اشتراک جدید استفاده کنید

✅ برای ادامه دکمه زیر را فشار دهید
"""

        keyboard = InlineKeyboardMarkup()
        keyboard.add(
            InlineKeyboardButton("ادامه خرید", callback_data="continue_buy")
        )

        bot.send_message(message.chat.id, text, reply_markup=keyboard)


# ---------------- ادامه خرید ----------------

    @bot.callback_query_handler(func=lambda call: call.data == "continue_buy")
    def continue_buy(call):

        text = "👈 لطفا یک گزینه را انتخاب کنید"

        keyboard = InlineKeyboardMarkup()
        keyboard.add(
            InlineKeyboardButton(
                "خرید با درگاه پرداخت مستقیم",
                callback_data="direct_payment"
            )
        )

        bot.edit_message_text(
            text,
            call.message.chat.id,
            call.message.message_id,
            reply_markup=keyboard
        )


# ---------------- انتخاب پلن ----------------

    @bot.callback_query_handler(func=lambda call: call.data == "direct_payment")
    def choose_plan(call):

        text = "💳 یکی از پلن های زیر را انتخاب کنید"

        keyboard = InlineKeyboardMarkup(row_width=1)

        keyboard.add(
            InlineKeyboardButton(
                "یک ماهه 36 گیگ - 128 هزار تومان",
                url=NEXT_PAY_LINKS["month1"]
            ),
            InlineKeyboardButton(
                "دو ماهه 78 گیگ - 198 هزار تومان",
                url=NEXT_PAY_LINKS["month2"]
            ),
            InlineKeyboardButton(
                "سه ماهه 127 گیگ - 329 هزار تومان",
                url=NEXT_PAY_LINKS["month3"]
            )
        )

        bot.edit_message_text(
            text,
            call.message.chat.id,
            call.message.message_id,
            reply_markup=keyboard
        )
