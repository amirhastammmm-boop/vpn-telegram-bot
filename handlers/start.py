from telegram import Update
from telegram.ext import ContextTypes
from keyboards import main_menu
from database import add_user_if_not_exists

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user

    referral_code = None
    if context.args:
        referral_code = context.args[0]

    add_user_if_not_exists(user.id, referral_code)

    await update.message.reply_text(
        "❤️ سلام دوست عزیز\n"
        "به ربات خوش اومدی\n\n"
        "یکی از گزینه ها رو انتخاب کن 👇",
        reply_markup=main_menu()
    )

def register_start_handlers(app):
    app.add_handler(CommandHandler("start", start))
