import logging
from aiogram import Bot, Dispatcher, types
from aiogram.client.default import DefaultBotProperties
from config import TOKEN


# --- BASE SETUP ---
logging.basicConfig(level=logging.INFO)

bot = Bot(
    token=TOKEN,
    default=DefaultBotProperties(parse_mode="HTML")
)
dp = Dispatcher()