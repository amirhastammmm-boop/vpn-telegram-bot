from database import create_tables
from bot import bot

create_tables()

print("Bot running...")
bot.infinity_polling()
