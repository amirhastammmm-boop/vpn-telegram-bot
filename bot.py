from telegram.ext import Application
from config import BOT_TOKEN
from handlers import register_handlers

app = Application.builder().token(BOT_TOKEN).build()

register_handlers(app)

if __name__ == "__main__":
    app.run_polling()
