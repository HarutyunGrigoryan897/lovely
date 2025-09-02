from aiogram.types import Message
from aiogram.filters import Command
from utils import create_user_in_django
from inline_keyboards import profile_about_kb, home_kb
from loader import dp, bot

@dp.message(Command("start"))
async def start_command(message: Message):
    user = message.from_user

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

        await message.answer_photo(photo=image_url, caption=text, reply_markup=profile_about_kb)
    else:
        await message.answer("❌ Something went wrong. Try again later.")


@dp.message(Command("help"))
async def help_command(message: Message):
    await message.answer("ℹ️ Available commands:\n/start - start the bot\n/help - show help")


@dp.message()
async def echo_handler(message: Message):
    """Echo handler for all other messages."""
    print(message.from_user.username)
    await message.answer(f"You said: {message.text}")