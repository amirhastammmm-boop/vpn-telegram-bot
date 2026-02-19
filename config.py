import os

BOT_TOKEN = os.getenv("BOT_TOKEN", "8443993110:AAH08NXvjcKty2XBHH13ecD8l5giSCD-ZF4")
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:password@localhost:5432/vpnbot_db")

SUPPORT_USERNAME = "@Amnbytry"
SECRET_KEY = os.getenv("SECRET_KEY", "CHANGE_THIS_SECRET_KEY")
