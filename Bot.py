from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from loader import dp
from payments import create_payment_link


# -----------------------
# منو خرید اشتراک
# -----------------------
@dp.message_handler(text="🛒 خرید اشتراک")
async def buy_menu(message: types.Message):

    keyboard = InlineKeyboardMarkup()
    keyboard.add(
        InlineKeyboardButton("ادامه خرید", callback_data="continue_buy")
    )

    text = """
🛒 منو خرید اشتراک:

⚠️ توجه داشته باشید هر باری که خرید میکنید یک اشتراک جدید با فایل های جدید دریافت میکنید و اشتراک هایی که قبلا تمام شده اند تمدید نمیشوند و باید از فایل های اشتراک جدید استفاده کنید

✅ برای ادامه دکمه زیر را فشار دهید
"""

    await message.answer(text, reply_markup=keyboard)


# -----------------------
# ادامه خرید
# -----------------------
@dp.callback_query_handler(lambda c: c.data == "continue_buy")
async def continue_buy(callback: types.CallbackQuery):

    keyboard = InlineKeyboardMarkup()
    keyboard.add(
        InlineKeyboardButton(
            "💳 خرید با درگاه پرداخت مستقیم",
            callback_data="direct_payment"
        )
    )

    await callback.message.edit_text(
        "👈 لطفا یک گزینه را انتخاب کنید",
        reply_markup=keyboard
    )


# -----------------------
# انتخاب درگاه مستقیم
# -----------------------
@dp.callback_query_handler(lambda c: c.data == "direct_payment")
async def direct_payment(callback: types.CallbackQuery):

    keyboard = InlineKeyboardMarkup(row_width=1)

    keyboard.add(
        InlineKeyboardButton(
            "یک کاربره یک ماهه 36 گیگابایت - 128 هزار تومان",
            callback_data="plan_1"
        )
    )

    keyboard.add(
        InlineKeyboardButton(
            "یک کاربره دو ماهه 78 گیگابایت - 198 هزار تومان",
            callback_data="plan_2"
        )
    )

    keyboard.add(
        InlineKeyboardButton(
            "یک کاربره سه ماهه 127 گیگابایت - 329 هزار تومان",
            callback_data="plan_3"
        )
    )

    await callback.message.edit_text(
        "📦 لطفا پلن مورد نظر را انتخاب کنید",
        reply_markup=keyboard
    )


# -----------------------
# انتخاب پلن ها
# -----------------------
@dp.callback_query_handler(lambda c: c.data.startswith("plan_"))
async def select_plan(callback: types.CallbackQuery):

    user_id = callback.from_user.id
    plan = callback.data

    if plan == "plan_1":
        price = 128000
        title = "اشتراک یک ماهه"

    elif plan == "plan_2":
        price = 198000
        title = "اشتراک دو ماهه"

    elif plan == "plan_3":
        price = 329000
        title = "اشتراک سه ماهه"

    # ساخت لینک پرداخت
    payment_url = await create_payment_link(user_id, price, title)

    keyboard = InlineKeyboardMarkup()
    keyboard.add(
        InlineKeyboardButton(
            "پرداخت",
            url=payment_url
        )
    )

    await callback.message.edit_text(
        f"✅ برای پرداخت روی دکمه زیر بزنید\n\n💰 مبلغ: {price} تومان",
        reply_markup=keyboard
    )
