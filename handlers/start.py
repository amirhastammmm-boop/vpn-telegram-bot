from telebot import types
from database import db
from keyboards.main_menu import main_menu


def generate_ref_code(user_id):
    return f"ref{user_id}"


def register_start_handlers(bot):

    @bot.message_handler(commands=['start'])
    def start_handler(message):

        user_id = message.from_user.id
        args = message.text.split()

        # ثبت کاربر
        if not db.user_exists(user_id):

            ref_by = None

            # اگر با رفرال وارد شده
            if len(args) > 1:
                ref_code = args[1]

                owner = db.get_user_by_ref(ref_code)

                if owner and owner != user_id:
                    ref_by = owner
                    db.add_points(owner, 1)

            db.add_user(
                user_id=user_id,
                ref_code=generate_ref_code(user_id),
                ref_by=ref_by
            )

        text = (
            "❤️ سلام دوست عزیز\n\n"
            "به ربات خوش اومدی\n"
            "لطفا یکی از گزینه ها را انتخاب کن 👇"
        )

        bot.send_message(
            message.chat.id,
            text,
            reply_markup=main_menu()
        )
