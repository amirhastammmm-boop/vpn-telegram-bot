from telegram.ext import MessageHandler, filters
from keyboards.main_menu import main_menu

async def tutorial(update, context):
    text = """1️⃣ WireGuard را نصب کنید.
2️⃣ فایل کانفیگ را Import کنید.
3️⃣ Connect را بزنید."""
    await update.message.reply_text(text, reply_markup=main_menu())

tutorial_handler = MessageHandler(filters.Regex("^آموزش$"), tutorial)
