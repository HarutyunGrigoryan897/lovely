import logging
from aiogram.types import Message
from aiogram.filters import Command
from utils import create_user_in_django, check_is_admin, get_admins_from_django
from inline_keyboards import profile_about_kb, home_kb, full_kb
from loader import dp, bot

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


logging.basicConfig(level=logging.INFO)

# -------------------- ADMIN FLOW --------------------
async def handle_admin_start(message: Message, user):
    text = (
        f"👑 Welcome Admin {user.first_name}!\n\n"
        f"Your Telegram ID: {user.id}\n"
        "You have admin privileges."
    )
    await message.answer(text)


# -------------------- USER FLOW --------------------
async def handle_user_start(message: Message, user):
    user_data = {
        "telegram_id": user.id,
        "username": user.username if user.username else user.id,
        "first_name": user.first_name or "",
        "last_name": user.last_name or "",
    }

    created_user = await create_user_in_django(user_data)

    if created_user:
        image_url = "https://img.freepik.com/free-vector/flea-market-concept-illustration_52683-55266.jpg"
        text = (
            f"👋 Welcome, {created_user.get('first_name') or ''}!\n\n"
            f"Username: @{created_user.get('username')}\n"
            f"Telegram ID: {created_user.get('telegram_id')}\n"
            f"Approved: {created_user.get('approved')}\n\n"
            "Enjoy using the bot!"
        )
        if created_user.get('approved') == False:
            await message.answer_photo(photo=image_url, caption=text, reply_markup=profile_about_kb)

            admins = await get_admins_from_django()
            if admins:
                notify_text = (
                    f"📢 New user registered!\n\n"
                    f"👤 {created_user.get('first_name')} {created_user.get('last_name')}\n"
                    f"🆔 Telegram ID: {created_user.get('telegram_id')}\n"
                    f"🔗 Username: @{created_user.get('username')}\n"
                )
                for admin in admins:
                    try:
                        profile_approved_kb = InlineKeyboardMarkup(
                                inline_keyboard=[
                                    [InlineKeyboardButton(text="✅ Approve", callback_data=f"approve:{created_user.get('telegram_id')}")],
                                    [InlineKeyboardButton(text="❌ Reject", callback_data=f"reject:{created_user.get('telegram_id')}")]
                                ]
                            )
                        await message.bot.send_message(
                            chat_id=admin["telegram_id"],
                            text=notify_text,
                            reply_markup=profile_approved_kb
                        )
                    except Exception as e:
                        logging.error(f"Failed to notify admin {admin}: {e}")
        else:
            await message.answer_photo(photo=image_url, caption=text, reply_markup=full_kb)

    else:
        await message.answer("❌ Something went wrong. Try again later.")


# -------------------- HANDLERS --------------------

@dp.message(Command("start"))
async def start_command(message: Message):
    user = message.from_user
    is_admin = await check_is_admin(user.id)

    if is_admin:
        await handle_admin_start(message, user)
    else:
        await handle_user_start(message, user)


@dp.message(Command("help"))
async def help_command(message: Message):
    await message.answer("ℹ️ Available commands:\n/start - start the bot\n/help - show help")


@dp.message()
async def echo_handler(message: Message):
    """Echo handler for all other messages."""
    await message.answer(f"You said: {message.text}")