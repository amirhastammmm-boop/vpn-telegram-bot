from telegram import Update
from telegram.ext import ContextTypes, MessageHandler, filters
from database import get_user_subscriptions

async def my_subs(update: Update, context: ContextTypes.DEFAULT_TYPE):
    subs = get_user_subscriptions(update.effective_user.id)

    if not subs:
        await update.message.reply_text("❌ اشتراکی نداری")
        return

    text = "📦 اشتراک های شما:\n\n"
    for sub in subs:
        text += f"کد: {sub}\n"

    await update.message.reply_text(text)

def register_my_sub_handlers(app):
    app.add_handler(MessageHandler(filters.Regex("📦 اشتراک های من"), my_subs))
