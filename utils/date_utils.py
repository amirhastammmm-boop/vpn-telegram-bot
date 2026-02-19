from datetime import datetime

def remaining_days(end_date):
    days = (end_date - datetime.now()).days
    return max(days, 0)
