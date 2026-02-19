from telegram.ext import MessageHandler, CallbackQueryHandler, filters
from keyboards.referral_menu import referral_menu
from keyboards.main_menu import main_menu
from services.user_service import get_user
from services.referral_service import redeem_subscription
from services.wireguard_service import generate_wireguard_config

async def show_referral(update, context):
    user_id = update.effective_user.id
    data = get_user(user_id)

    referral_code, points = data

    text = f"""
کد رفرال شما:
{referral_code}

با هر دعوت = ۱ امتیاز
با هر خرید دعوت‌شده = ۱ امتیاز

امتیاز فعلی شما: {points}
"""

    await update.message.reply_text(text, reply_markup=referral_menu())

async def redeem(update, context):
    query = update.callback_query
    await query.answer()

    user_id = query.from_user.id
    data = get_user(user_id)
    points = data[1]

    if points < 5:
        await query.message.reply_text("امتیاز کافی ندارید.", reply_markup=main_menu())
        return

    sub_id = redeem_subscription(user_id)
    config = generate_wireguard_config()

    await query.message.reply_document(
        document=config.encode(),
        filename=f"{sub_id}.conf"
    )

    await query.message.reply_text("اشتراک رایگان فعال شد ✅", reply_markup=main_menu())

referral_handler = MessageHandler(filters.Regex("^امتیازهای من$"), show_referral)
redeem_handler = CallbackQueryHandler(redeem, pattern="^redeem$")
