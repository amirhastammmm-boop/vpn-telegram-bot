from telegram import Update
from telegram.ext import ContextTypes, MessageHandler, filters
from database import get_user_points, get_referral_code

async def points(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    points = get_user_points(user_id)
    ref_code = get_referral_code(user_id)

    text = (
        f"🏆 امتیاز شما: {points}\n\n"
        f"کد رفرال شما:\n{ref_code}\n\n"
        "هر 5 امتیاز = 1 ماه اشتراک رایگان\n"
        "هر 8 امتیاز = 1 ماه اشتراک رایگان"
    )

    await update.message.reply_text(text)

def register_points_handlers(app):
    app.add_handler(MessageHandler(filters.Regex("🏆 امتیاز های من"), points))
