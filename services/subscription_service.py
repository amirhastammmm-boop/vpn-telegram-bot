import uuid
from datetime import datetime, timedelta
from database import get_cursor

def create_subscription(user_id, months, gb):
    cur = get_cursor()

    sub_id = str(uuid.uuid4())
    start = datetime.now()
    end = start + timedelta(days=30*months)

    cur.execute("""
        INSERT INTO subscriptions
        VALUES(%s,%s,%s,%s,%s,%s,%s,'active')
    """,(sub_id,user_id,months,start,end,gb,gb))

    return sub_id

def get_user_subscriptions(user_id):
    cur = get_cursor()
    cur.execute("SELECT * FROM subscriptions WHERE user_id=%s",(user_id,))
    return cur.fetchall()
