import uuid
import os
import psycopg2
from datetime import datetime, timedelta
from telegram import Update, ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, CallbackQueryHandler, ContextTypes, filters

TOKEN = "8443993110:AAH08NXvjcKty2XBHH13ecD8l5giSCD-ZF4"
SUPPORT_ID = "Amnbytry@"
DATABASE_URL = os.getenv("DATABASE_URL","postgresql://user:password@localhost:5432/vpnbot")

app = ApplicationBuilder().token(TOKEN).build()
conn = psycopg2.connect(DATABASE_URL)
conn.autocommit = True
cur = conn.cursor()

cur.execute("CREATE TABLE IF NOT EXISTS users(user_id BIGINT PRIMARY KEY,referral_code TEXT UNIQUE,points INT DEFAULT 0,invited_by BIGINT)")
cur.execute("CREATE TABLE IF NOT EXISTS subscriptions(id TEXT PRIMARY KEY,user_id BIGINT,plan_months INT,start_date TIMESTAMP,end_date TIMESTAMP,total_gb INT,remaining_gb INT)")

def main_menu():
    return ReplyKeyboardMarkup(
        [["خرید اشتراک","اشتراک‌های من"],
         ["امتیازهای من","آموزش"],
         ["پشتیبانی"]],
        resize_keyboard=True,
        one_time_keyboard=False
    )

def register_user(user_id,ref=None):
    cur.execute("SELECT user_id FROM users WHERE user_id=%s",(user_id,))
    if not cur.fetchone():
        referral_code=f"REF{user_id}"
        invited_by=int(ref) if ref and ref.isdigit() else None
        cur.execute("INSERT INTO users(user_id,referral_code,points,invited_by) VALUES(%s,%s,%s,%s)",(user_id,referral_code,0,invited_by))

def create_subscription(user_id,months,gb):
    sub_id=str(uuid.uuid4())[:8]
    start=datetime.now()
    end=start+timedelta(days=30*months)
    cur.execute("INSERT INTO subscriptions VALUES(%s,%s,%s,%s,%s,%s,%s)",(sub_id,user_id,months,start,end,gb,gb))
    config=f"""[Interface]
PrivateKey = AUTO_PRIVATE_KEY
Address = 10.0.0.2/32
DNS = 1.1.1.1

[Peer]
PublicKey = SERVER_PUBLIC_KEY
Endpoint = server_ip:51820
AllowedIPs = 0.0.0.0/0"""
    return sub_id,config

async def start(update:Update,context:ContextTypes.DEFAULT_TYPE):
    user_id=update.effective_user.id
    ref=context.args[0] if context.args else None
    register_user(user_id,ref)
    await update.message.reply_text("به ربات Payydar VPN خوش آمدید 👋",reply_markup=main_menu())

async def buy_menu(update:Update,context:ContextTypes.DEFAULT_TYPE):
    kb=[[InlineKeyboardButton("اشتراک ۱ ماهه | ۳۳ گیگ | ۱۳۰,۰۰۰ تومان",callback_data="1")],
        [InlineKeyboardButton("اشتراک ۲ ماهه | ۷۷ گیگ | ۲۶۰,۰۰۰ تومان",callback_data="2")],
        [InlineKeyboardButton("اشتراک ۳ ماهه | ۱۱۰ گیگ | ۳۹۰,۰۰۰ تومان",callback_data="3")]]
    await update.message.reply_text("یکی از پلن‌ها را انتخاب کنید:",reply_markup=InlineKeyboardMarkup(kb))

async def handle_plan(update:Update,context:ContextTypes.DEFAULT_TYPE):
    q=update.callback_query
    await q.answer()
    user_id=q.from_user.id
    plans={"1":(1,33),"2":(2,77),"3":(3,110)}
    months,gb=plans[q.data]
    payment_link=f"https://yourpaymentgateway.com/pay?plan={months}"
    await q.message.reply_text(f"لینک پرداخت:\n{payment_link}")
    sub_id,config=create_subscription(user_id,months,gb)
    await q.message.reply_document(document=config.encode(),filename=f"{sub_id}.conf")
    await q.message.reply_text("اشتراک فعال شد ✅",reply_markup=main_menu())

async def my_subs(update:Update,context:ContextTypes.DEFAULT_TYPE):
    user_id=update.effective_user.id
    cur.execute("SELECT * FROM subscriptions WHERE user_id=%s",(user_id,))
    rows=cur.fetchall()
    if not rows:
        await update.message.reply_text("شما اشتراکی ندارید.",reply_markup=main_menu())
        return
    text=""
    for r in rows:
        remaining=(r[4]-datetime.now()).days
        text+=f"\nکد:{r[0]}\nپلن:{r[2]} ماهه\nشروع:{r[3].date()}\nپایان:{r[4].date()}\nروز باقی‌مانده:{remaining}\nحجم کل:{r[5]}GB\nحجم باقی‌مانده:{r[6]}GB\n"
    await update.message.reply_text(text,reply_markup=main_menu())

async def points(update:Update,context:ContextTypes.DEFAULT_TYPE):
    user_id=update.effective_user.id
    cur.execute("SELECT referral_code,points FROM users WHERE user_id=%s",(user_id,))
    data=cur.fetchone()
    kb=[[InlineKeyboardButton("دریافت اشتراک با امتیاز",callback_data="redeem")]]
    text=f"کد رفرال شما:\n{data[0]}\n\nبا هر دعوت=1 امتیاز\nبا هر خرید دعوت‌شده=1 امتیاز\n\nامتیاز فعلی:{data[1]}"
    await update.message.reply_text(text,reply_markup=InlineKeyboardMarkup(kb))

async def redeem(update:Update,context:ContextTypes.DEFAULT_TYPE):
    q=update.callback_query
    await q.answer()
    user_id=q.from_user.id
    cur.execute("SELECT points FROM users WHERE user_id=%s",(user_id,))
    pts=cur.fetchone()[0]
    if pts>=5:
        cur.execute("UPDATE users SET points=points-5 WHERE user_id=%s",(user_id,))
        sub_id,config=create_subscription(user_id,1,33)
        await q.message.reply_document(document=config.encode(),filename=f"{sub_id}.conf")
        await q.message.reply_text("اشتراک رایگان فعال شد ✅",reply_markup=main_menu())
    else:
        await q.message.reply_text("امتیاز کافی ندارید.",reply_markup=main_menu())

async def tutorial(update:Update,context:ContextTypes.DEFAULT_TYPE):
    text="1️⃣ WireGuard را نصب کنید.\n2️⃣ فایل کانفیگ را Import کنید.\n3️⃣ Connect را بزنید."
    await update.message.reply_text(text,reply_markup=main_menu())

async def support(update:Update,context:ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"در صورت بروز مشکل به پشتیبانی پیام دهید:\n{SUPPORT_ID}",reply_markup=main_menu())

app.add_handler(CommandHandler("start",start))
app.add_handler(MessageHandler(filters.Regex("^خرید اشتراک$"),buy_menu))
app.add_handler(MessageHandler(filters.Regex("^اشتراک‌های من$"),my_subs))
app.add_handler(MessageHandler(filters.Regex("^امتیازهای من$"),points))
app.add_handler(MessageHandler(filters.Regex("^آموزش$"),tutorial))
app.add_handler(MessageHandler(filters.Regex("^پشتیبانی$"),support))
app.add_handler(CallbackQueryHandler(handle_plan,pattern="^[123]$"))
app.add_handler(CallbackQueryHandler(redeem,pattern="^redeem$"))

app.run_polling()
