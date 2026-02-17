from telegram import (
    Update,
    ReplyKeyboardMarkup,
    KeyboardButton
)

from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters
)

from config import TOKEN, BOT_USERNAME
from database import add_user, get_points, get_ref_count


# -------- منو --------

def main_menu():

    keyboard = [
        [KeyboardButton("💳 خرید اشتراک"), KeyboardButton("📦 اشتراک های من")],
        [KeyboardButton("🏆 امتیاز های من"), KeyboardButton("📚 آموزش ربات")],
        [KeyboardButton("🛠 پشتیبانی")]
    ]

    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)


# -------- start --------

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_id = update.effective_user.id
    inviter = None

    # دریافت لینک رفرال
    if context.args:
        try:
            ref = int(context.args[0])

            if ref != user_id:
                inviter = ref
        except:
            pass

    add_user(user_id, inviter)

    text = """
♥️سلام دوست عزیز

به ربات پینگ خور خوش اومدی

⬇️لطفا یک گزینه رو انتخاب کن
"""

    await update.message.reply_text(text, reply_markup=main_menu())


# -------- امتیاز ها --------

async def points(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_id = update.effective_user.id

    points = get_points(user_id)
    refs = get_ref_count(user_id)

    ref_link = f"https://t.me/{BOT_USERNAME}?start={user_id}"

    text = f"""
🏆با معرفی کردن پینگ خور به دیگران، کسب امتیاز کنید و اشتراک رایگان دریافت کنید!



✅لینک اختصاصی خودتون رو از پایین همین پیام کپی کنید و در گروه ها و کانال های مختلف و شبکه های اجتماعی به اشتراک بگذارید و هر فردی که روی لینک شما کلیک کنه وارد ربات میشه و این فرد به عنوان زیر مجموعه شما ذخیره میشه و با هر خریدی که این فرد انجام بده، به شما امتیاز تعلق میگیره و شما میتونید از امتیازات کسب شده به جای پول استفاده کنید و اشتراک بخرید



✅با خرید اکانت یک ماهه توسط زیر مجموعه های شما، 1 امتیاز  و با خرید اکانت 2 ماهه، 2 امتیاز و با خرید اکانت 3 ماهه 3 امتیاز به شما تعلق میگیره همچنین با خرید هایی که زیر مجموعه های شما در ماه های بعد انجام میدهند باز هم به شما امتیاز تعلق میگیره و همچنین میتونید بی نهایت زیرمجموعه کسب کنید



⭕️نکته: افرادی که روی لینک شما کلیک میکنن باید قبلا خریدی انجام نداده باشن در غیر اینصورت به عنوان زیر مجموعه شما ذخیره نمیشن

🎖تعداد امتیازهای شما         : {points}
🙍‍♂️تعداد زیرمجموعه های شما: {refs}
🌍لینک اخصاصی شما(👇)

{ref_link}
"""

    await update.message.reply_text(text)


# -------- آموزش --------

async def tutorial(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(
        "📚 آموزش استفاده از Wireguard بزودی اضافه میشود"
    )


# -------- پشتیبانی --------

async def support(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(
        "جهت پشتیبانی به آیدی زیر پیام دهید:\n@633464148"
    )


# -------- هندل پیام --------

async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):

    text = update.message.text

    if text == "🏆 امتیاز های من":
        await points(update, context)

    elif text == "📚 آموزش ربات":
        await tutorial(update, context)

    elif text == "🛠 پشتیبانی":
        await support(update, context)


# -------- اجرا --------

def main():

    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))

    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message_handler))

    print("Bot Started...")
    app.run_polling()


if __name__ == "__main__":
    main()
