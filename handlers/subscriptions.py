from telegram.ext import MessageHandler, filters
from keyboards.main_menu import main_menu
from services.subscription_service import get_user_subscriptions
from utils.date_utils import remaining_days

async def my_subscriptions(update, context):
    user_id = update.effective_user.id
    subs = get_user_subscriptions(user_id)

    if not subs:
        await update.message.reply_text("شما اشتراکی ندارید.", reply_markup=main_menu())
        return

    text = ""
    for s in subs:
        days = remaining_days(s[4])
        text += f"""
کد اشتراک: {s[0]}
پلن: {s[2]} ماهه
شروع: {s[3].date()}
پایان: {s[4].date()}
روز باقی‌مانده: {days}
حجم کل: {s[5]}GB
حجم باقی‌مانده: {s[6]}GB
---------------------
"""

    await update.message.reply_text(text, reply_markup=main_menu())

subscriptions_handler = MessageHandler(filters.Regex("^اشتراک‌های من$"), my_subscriptions)
