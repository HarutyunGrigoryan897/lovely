from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo

home_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="🏠 Home", callback_data="home")]
    ]
)


profile_about_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="👤 Profile", callback_data="profile")],
        [InlineKeyboardButton(text="ℹ️ About our service", callback_data="about")]
    ]
)


full_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="🛒 Catalog", callback_data="catalog", web_app=WebAppInfo(url="http://127.0.0.1:8000/"))],
        [InlineKeyboardButton(text="📦 Orders", callback_data="orders")],
        [InlineKeyboardButton(text="👤 Profile", callback_data="profile")],
        [InlineKeyboardButton(text="ℹ️ About our service", callback_data="about")]
    ]
)
