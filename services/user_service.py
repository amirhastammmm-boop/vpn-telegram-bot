import hashlib
from config import SECRET_KEY
from database import get_cursor

def generate_referral_code(user_id):
    raw = f"{user_id}{SECRET_KEY}"
    return hashlib.sha256(raw.encode()).hexdigest()[:10]

def register_user(user_id, ref=None):
    cur = get_cursor()

    cur.execute("SELECT user_id FROM users WHERE user_id=%s", (user_id,))
    if cur.fetchone():
        return

    referral_code = generate_referral_code(user_id)

    invited_by = None
    if ref:
        cur.execute("SELECT user_id FROM users WHERE referral_code=%s", (ref,))
        row = cur.fetchone()
        if row:
            invited_by = row[0]
            cur.execute("UPDATE users SET points = points + 1 WHERE user_id=%s", (invited_by,))

    cur.execute("""
        INSERT INTO users(user_id, referral_code, invited_by)
        VALUES(%s,%s,%s)
    """,(user_id, referral_code, invited_by))

def get_user(user_id):
    cur = get_cursor()
    cur.execute("SELECT referral_code, points FROM users WHERE user_id=%s",(user_id,))
    return cur.fetchone()

def deduct_points(user_id, amount):
    cur = get_cursor()
    cur.execute("UPDATE users SET points = points - %s WHERE user_id=%s",(amount,user_id))
