from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from config import WEB_APP_URL

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
        [InlineKeyboardButton(text="🛒 Catalog", web_app=WebAppInfo(url=f"{WEB_APP_URL}webapp_telegram/index/"))],
        [InlineKeyboardButton(text="📦 Orders", web_app=WebAppInfo(url=f"{WEB_APP_URL}webapp_telegram/orders/"))],
        [InlineKeyboardButton(text="👤 Profile", callback_data="profile")],
        [InlineKeyboardButton(text="ℹ️ About our service", callback_data="about")]
    ]
)

admin_info_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="🙋‍♂️ Waiting Approve", callback_data="admin_waiting_approve")],
        [InlineKeyboardButton(text="🤷‍♂️ Waiting Status Set", callback_data="admin_waiting_status_set")],
        [InlineKeyboardButton(text="📦 Order Waiting Confirm", callback_data="order_waiting_confirm")],
        [InlineKeyboardButton(text="🚢 Order Waiting Shiping", callback_data="admin_waiting_shipping")],
        [InlineKeyboardButton(text="💼 Last 10 Shipped Orders", callback_data="last_10_orders")]
    ]
)