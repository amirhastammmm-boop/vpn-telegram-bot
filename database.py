import psycopg2
from config import DATABASE_URL

conn = psycopg2.connect(DATABASE_URL)
conn.autocommit = True

def get_cursor():
    return conn.cursor()
