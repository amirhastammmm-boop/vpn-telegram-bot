import telebot
from config import BOT_TOKEN
from handlers import register_handlers

bot = telebot.TeleBot(BOT_TOKEN)

register_handlers(bot)

print("Bot is running...")

bot.infinity_polling()
