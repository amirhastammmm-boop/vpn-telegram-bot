from database import get_cursor

def create_tables():
    cur = get_cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS users(
        user_id BIGINT PRIMARY KEY,
        referral_code TEXT UNIQUE,
        points INT DEFAULT 0,
        invited_by BIGINT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS subscriptions(
        id TEXT PRIMARY KEY,
        user_id BIGINT,
        plan_months INT,
        start_date TIMESTAMP,
        end_date TIMESTAMP,
        total_gb INT,
        remaining_gb INT,
        status TEXT DEFAULT 'active'
    )
    """)
