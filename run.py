from database import create_tables, create_users_table
from bot import bot   # اگر اسم فایل بوتت چیز دیگه بود بگو اصلاح کنم

# ساخت جدول ها
create_tables()
create_users_table()

# اجرای ربات
bot.run()
