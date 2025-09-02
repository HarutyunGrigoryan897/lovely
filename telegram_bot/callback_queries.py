from loader import dp, bot
from aiogram import types, F
from aiogram.types import Message, CallbackQuery
from inline_keyboards import profile_about_kb, home_kb, full_kb
from utils import get_user_info, update_user_status

# -------------------- USER FLOW --------------------
@dp.callback_query(lambda c: c.data == "about")
async def about_callback(query: CallbackQuery):
    text = (
        "ℹ️ About our service:\n\n"
        "Here you can write your full description text of the service.\n"
        "Include benefits, prices, or anything you want users to know."
    )
    await query.message.answer(text, reply_markup=home_kb)
    await query.answer()


@dp.callback_query(lambda c: c.data == "profile")
async def profile_callback(query: CallbackQuery):
    telegram_id = query.from_user.id
    user_info = await get_user_info(telegram_id)

    if user_info:
        text = (
            f"👤 Your Profile:\n\n"
            f"Username: @{user_info.get('username') or '—'}\n"
            f"First Name: {user_info.get('first_name') or '—'}\n"
            f"Last Name: {user_info.get('last_name') or '—'}\n"
            f"Telegram ID: {user_info.get('telegram_id')}\n"
            f"Approved: {user_info.get('approved')}\n"
            f"Joind data: {user_info.get('date_joined')}\n"
        )
        await query.message.answer(text, reply_markup=home_kb)
    else:
        await query.message.answer("❌ Could not fetch profile. Try again later.", reply_markup=home_kb)

    await query.answer()


@dp.callback_query(lambda c: c.data == "home")
async def home_callback(query: CallbackQuery):
    telegram_id = query.from_user.id
    user_info = await get_user_info(telegram_id)

    if user_info:
        image_url = "https://img.freepik.com/free-vector/flea-market-concept-illustration_52683-55266.jpg"
        text = (
            f"👋 Welcome, {user_info.get('first_name') or ''}!\n\n"
            f"Username: @{user_info.get('username')}\n"
            f"Telegram ID: {user_info.get('telegram_id')}\n"
            f"Approved: {user_info.get('approved')}\n"
            f"Joind data: {user_info.get('date_joined')}\n\n"

            "Enjoy using the bot!"
        )
        if user_info.get('approved') == True:
            # await bot.set_chat_menu_button(
            #         menu_button=types.MenuButtonWebApp(
            #             text="Каталог",
            #             web_app=types.WebAppInfo(url="https://yourserver.com/app/")
            #         )
            #     )
            await query.message.answer_photo(photo=image_url, caption=text, reply_markup=full_kb)
        else:
            await query.message.answer_photo(photo=image_url, caption=text, reply_markup=profile_about_kb)

    else:
        await query.message.answer("❌ Could not fetch profile. Try again later.", reply_markup=home_kb)

    await query.answer()

# -------------------- ADMIN FLOW --------------------
@dp.callback_query(F.data.startswith("approve:"))
async def approve_user_callback(callback: CallbackQuery):
    telegram_id = int(callback.data.split(":")[1])
    success = await update_user_status(telegram_id, approve=True)

    if success:
        await callback.message.delete()
        await callback.message.answer("✅ User approved successfully.")
        await callback.bot.send_message(
            chat_id=telegram_id,
            text="🎉 Your profile has been approved! You can start shopping now.",
            reply_markup=full_kb
        )
    else:
        await callback.message.answer("❌ Failed to approve user.")


@dp.callback_query(F.data.startswith("reject:"))
async def reject_user_callback(callback: CallbackQuery):
    telegram_id = int(callback.data.split(":")[1])
    success = await update_user_status(telegram_id, approve=False)

    if success:
        await callback.message.delete()
        await callback.message.answer("❌ User rejected.")
        await callback.bot.send_message(
            chat_id=telegram_id,
            text="⚠️ Your registration request was rejected by the admin."
        )
    else:
        await callback.message.answer("❌ Failed to reject user.")