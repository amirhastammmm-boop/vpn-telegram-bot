from telegram.ext import ApplicationBuilder
from config import BOT_TOKEN
from models import create_tables

from handlers.start import start_handler
from handlers.buy import buy_handler, plan_handler
from handlers.subscriptions import subscriptions_handler
from handlers.referral import referral_handler, redeem_handler
from handlers.tutorial import tutorial_handler
from handlers.support import support_handler

app = ApplicationBuilder().token(BOT_TOKEN).build()

create_tables()

app.add_handler(start_handler)
app.add_handler(buy_handler)
app.add_handler(plan_handler)
app.add_handler(subscriptions_handler)
app.add_handler(referral_handler)
app.add_handler(redeem_handler)
app.add_handler(tutorial_handler)
app.add_handler(support_handler)

app.run_polling()
