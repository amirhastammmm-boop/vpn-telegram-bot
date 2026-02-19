from services.subscription_service import create_subscription
from services.user_service import deduct_points

def redeem_subscription(user_id):
    sub_id = create_subscription(user_id, 1, 33)
    deduct_points(user_id, 5)
    return sub_id
