from telegram import Update
from telegram.ext import ContextTypes, MessageHandler, filters
from keyboards import buy_menu, main_menu

async def buy_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "پلن مورد نظر رو انتخاب کن:",
        reply_markup=buy_menu()
    )

async def buy_plan(update: Update, context: ContextTypes.DEFAULT_TYPE):
    plan = update.message.text

    if plan == "🔙 بازگشت":
        await update.message.reply_text("برگشتی به منو اصلی", reply_markup=main_menu())
        return

    await update.message.reply_text(
        f"شما پلن {plan} رو انتخاب کردی.\nبعداً اینجا پرداخت وصل میشه."
    )

def register_buy_handlers(app):
    app.add_handler(MessageHandler(filters.Regex("🛒 خرید اشتراک"), buy_handler))
    app.add_handler(MessageHandler(filters.Regex("1 ماهه|2 ماهه|3 ماهه|🔙 بازگشت"), buy_plan))
async def support(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "در صورت نیاز به پشتیبانی به آیدی زیر پیام دهید:\n@Amnbytry"
    )

async def tutorial(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "فایل WireGuard و آموزش نصب بعداً اینجا ارسال میشه."
    )
