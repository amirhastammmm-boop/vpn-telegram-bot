import requests
from config import NEXT_PAY_API_KEY, CALLBACK_URL


def create_payment(amount):
    url = "https://nextpay.org/nx/gateway/token"

    data = {
        "api_key": NEXT_PAY_API_KEY,
        "amount": amount,
        "callback_uri": CALLBACK_URL
    }

    r = requests.post(url, json=data).json()

    if r["code"] == 200:
        token = r["trans_id"]
        return f"https://nextpay.org/nx/gateway/payment/{token}"

    return None
