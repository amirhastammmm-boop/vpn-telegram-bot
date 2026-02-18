from telebot import TeleBot
import config
from database import create_tables
from handlers import register_handlers

bot = TeleBot(config.BOT_TOKEN)

create_tables()
register_handlers(bot)

bot.infinity_polling()
