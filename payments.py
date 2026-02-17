import aiohttp
from config import NEXT_PAY_API_KEY, CALLBACK_URL


async def create_payment_link(user_id, amount, title):

    url = "https://nextpay.org/nx/gateway/token"

    payload = {
        "api_key": NEXT_PAY_API_KEY,
        "amount": amount,
        "callback_uri": CALLBACK_URL,
        "order_id": str(user_id),
        "description": title
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=payload) as resp:

            data = await resp.json()

            if data["code"] == -1:
                token = data["trans_id"]
                return f"https://nextpay.org/nx/gateway/payment/{token}"

            return "خطا در ساخت لینک پرداخت"
