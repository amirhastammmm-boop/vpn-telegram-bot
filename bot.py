from telebot import TeleBot
import os
from database import create_tables
from handlers import register_handlers

TOKEN = os.getenv("BOT_TOKEN")

bot = TeleBot(TOKEN)

create_tables()
register_handlers(bot)

bot.infinity_polling()
