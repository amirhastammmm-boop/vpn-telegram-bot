from database import create_tables, create_users_table
from bot import bot

# ساخت جدول های دیتابیس
create_tables()
create_users_table()

# اجرای ربات
print("Bot is running...")
bot.infinity_polling()
