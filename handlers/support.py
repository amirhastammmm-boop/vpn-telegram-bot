from telegram.ext import MessageHandler, filters
from keyboards.main_menu import main_menu
from config import SUPPORT_USERNAME

async def support(update, context):
    await update.message.reply_text(
        f"در صورت بروز مشکل به پشتیبانی پیام دهید:\n{SUPPORT_USERNAME}",
        reply_markup=main_menu()
    )

support_handler = MessageHandler(filters.Regex("^پشتیبانی$"), support)
