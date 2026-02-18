from database import add_subscription
from datetime import datetime, timedelta


@bot.message_handler(commands=['testsub'])
def test_sub(message):

    user_id = message.from_user.id

    buy_date = datetime.now().strftime("%Y-%m-%d")
    expire_date = (datetime.now() + timedelta(days=30)).strftime("%Y-%m-%d")

    data = (
        user_id,
        buy_date,
        expire_date,
        "36GB",
        "TEST_PRIVATE_KEY",
        "10.0.0.2/32",
        "TEST_SERVER_KEY",
        "1.1.1.1:51820"
    )

    add_subscription(data)

    bot.send_message(message.chat.id, "✅ اشتراک تستی ساخته شد")
