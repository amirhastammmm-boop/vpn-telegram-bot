import os
import telebot
from handlers import register_handlers

# گرفتن توکن از Railway ENV
BOT_TOKEN = os.getenv("BOT_TOKEN")

if not BOT_TOKEN:
    raise Exception("BOT_TOKEN not found in environment variables")

# ساخت ربات
bot = telebot.TeleBot(BOT_TOKEN)

# ثبت همه هندلرها
register_handlers(bot)


# اجرا
if __name__ == "__main__":
    print("Bot is running...")
    bot.infinity_polling(skip_pending=True)
