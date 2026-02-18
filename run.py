from database import create_tables, create_users_table
from bot import bot


def main():
    # ساخت جدول‌های دیتابیس
    create_tables()
    create_users_table()

    print("Bot is running...")
    bot.infinity_polling(skip_pending=True)


if __name__ == "__main__":
    main()
