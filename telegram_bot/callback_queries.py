from loader import dp, bot
from aiogram import types, F
from aiogram.types import Message, CallbackQuery
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from inline_keyboards import profile_about_kb, home_kb, full_kb, admin_info_kb
from utils import get_user_info, update_user_status, get_waiting_approved_users, get_waiting_status_users

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
    """First step: Show level selection buttons (user not approved yet)"""
    telegram_id = int(callback.data.split(":")[1])
    
    # Get user info to display
    user_info = await get_user_info(telegram_id)
    
    if user_info:
        # Show level selection buttons to admin
        level_selection_kb = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="👤 User", callback_data=f"setlevel:USER:{telegram_id}")],
                [InlineKeyboardButton(text="💼 Dealer", callback_data=f"setlevel:DEALER:{telegram_id}")],
                [InlineKeyboardButton(text="⭐ VIP", callback_data=f"setlevel:VIP:{telegram_id}")],
                [InlineKeyboardButton(text="🤝 Partner", callback_data=f"setlevel:PARTNER:{telegram_id}")],
                [InlineKeyboardButton(text="❌ Cancel", callback_data=f"reject:{telegram_id}")]
            ]
        )
        await callback.message.answer(
            f"📋 Approving user:\n"
            f"👤 {user_info.get('first_name', '')} {user_info.get('last_name', '')}\n"
            f"🆔 Telegram ID: {user_info.get('telegram_id')}\n"
            f"🔗 Username: @{user_info.get('username', 'N/A')}\n\n"
            "Please select the user level:",
            reply_markup=level_selection_kb
        )
        await callback.message.delete()
        await callback.answer()
    else:
        await callback.message.answer("❌ Failed to fetch user information.")
        await callback.answer()


@dp.callback_query(F.data.startswith("setlevel:"))
async def set_level_callback(callback: CallbackQuery):
    """Handle user level selection and approve user"""
    from utils import set_user_level, update_user_status
    
    parts = callback.data.split(":")
    level_name = parts[1]
    telegram_id = int(parts[2])
    
    # First, set the user level
    result = await set_user_level(telegram_id, level_name)
    
    if result:
        # Now approve the user
        approval_success = await update_user_status(telegram_id, approve=True)
        
        if approval_success:
            level_display = {
                'USER': '👤 User',
                'DEALER': '💼 Dealer',
                'VIP': '⭐ VIP',
                'PARTNER': '🤝 Partner'
            }.get(level_name, level_name)
            
            await callback.message.answer(
                f"✅ User with Telegram ID:{telegram_id}\n approved successfully!\n\n"
                f"📊 Level set to: {level_display}\n"
                f"💰 Price multiplier: {result.get('multiplier', 'N/A')}",
                reply_markup=admin_info_kb
            )
            await callback.message.delete()
            
            # Notify the user
            await callback.bot.send_message(
                chat_id=telegram_id,
                text=f"🎉 Your profile has been approved!\n\n"
                     f"📊 Your level: {level_display}\n"
                     f"You can start shopping now!",
                reply_markup=full_kb
            )
            await callback.answer("✅ User approved and level set!")
        else:
            await callback.message.answer("⚠️ Level was set but failed to approve user.")
            await callback.answer()
    else:
        await callback.message.answer("❌ Failed to set user level.")
        await callback.answer()


@dp.callback_query(F.data.startswith("reject:"))
async def reject_user_callback(callback: CallbackQuery):
    telegram_id = int(callback.data.split(":")[1])
    success = await update_user_status(telegram_id, approve=False)

    if success:
        await callback.message.edit_text("❌ User registration rejected.")
        await callback.bot.send_message(
            chat_id=telegram_id,
            text="⚠️ Your registration request was rejected by the admin."
        )
        await callback.answer("User rejected")
    else:
        await callback.message.answer("❌ Failed to reject user.")
        await callback.answer()


# -------------------- ORDER MANAGEMENT FLOW --------------------
@dp.callback_query(F.data.startswith("order_approve:"))
async def approve_order_callback(callback: CallbackQuery):
    """Handle order approval"""
    order_id = int(callback.data.split(":")[1])
    
    try:
        # Here you can add logic to update order status in Django
        # For now, just update the message
        await callback.message.edit_text(
            f"✅ Order #{order_id} has been ACCEPTED!\n\n"
            f"The customer will be notified and the order will be processed.\n"
            f"📦 Please prepare the items for shipping.\n\n"
            f"✨ Order accepted by: @{callback.from_user.username or callback.from_user.first_name}"
        )
        await callback.answer("✅ Order accepted successfully!")
    except Exception as e:
        await callback.answer(f"❌ Error: {str(e)}", show_alert=True)


@dp.callback_query(F.data.startswith("order_reject:"))
async def reject_order_callback(callback: CallbackQuery):
    """Handle order rejection"""
    order_id = int(callback.data.split(":")[1])
    
    try:
        # Here you can add logic to update order status in Django
        await callback.message.edit_text(
            f"❌ Order #{order_id} has been DECLINED!\n\n"
            f"⚠️ The customer will need to be notified about the cancellation.\n"
            f"Please provide a reason for rejection if necessary.\n\n"
            f"🚫 Order declined by: @{callback.from_user.username or callback.from_user.first_name}"
        )
        await callback.answer("Order declined")
    except Exception as e:
        await callback.answer(f"❌ Error: {str(e)}", show_alert=True)


@dp.callback_query(F.data.startswith("order_view:"))
async def view_order_callback(callback: CallbackQuery):
    """Handle view order details request"""
    order_id = int(callback.data.split(":")[1])
    
    try:
        # For now, just acknowledge the callback
        # You can add logic to fetch more details from Django API
        await callback.answer(
            f"📋 Order #{order_id} - Full details available in admin panel",
            show_alert=True
        )
    except Exception as e:
        await callback.answer(f"❌ Error: {str(e)}", show_alert=True)

@dp.callback_query(lambda c: c.data == "admin_waiting_approve")
async def admin_waiting_approve_callback(callback: CallbackQuery):
    data = await get_waiting_approved_users()
    if data:
        for user in data:
            notify_text = (
                f"👤 {user.get('first_name')} {user.get('last_name')}\n"
                f"🆔 Telegram ID: {user.get('telegram_id')}\n"
                f"🔗 Username: @{user.get('username')}\n"
            )
            try:
                profile_approved_kb = InlineKeyboardMarkup(
                        inline_keyboard=[
                            [InlineKeyboardButton(text="✅ Approve", callback_data=f"approve:{user.get('telegram_id')}")],
                            [InlineKeyboardButton(text="❌ Reject", callback_data=f"reject:{user.get('telegram_id')}")]
                        ]
                    )
                await callback.message.answer(
                    text=notify_text,
                    reply_markup=profile_approved_kb
                )
            except Exception as e:
                await callback.answer("❌ Something went wrong. Try again later.")
        await callback.answer()
    else:
        await callback.message.answer("🌟 There all users are approved", reply_markup=admin_info_kb)
        await callback.answer()
    await callback.message.delete()

@dp.callback_query(lambda c: c.data == "admin_waiting_status_set")
async def admin_waiting_status_callback(callback: CallbackQuery):
    data = await get_waiting_status_users()
    if data:
        for user in data:
            try:
                level_selection_kb = InlineKeyboardMarkup(
                    inline_keyboard=[
                        [InlineKeyboardButton(text="👤 User", callback_data=f"setlevel:USER:{user.get('telegram_id')}")],
                        [InlineKeyboardButton(text="💼 Dealer", callback_data=f"setlevel:DEALER:{user.get('telegram_id')}")],
                        [InlineKeyboardButton(text="⭐ VIP", callback_data=f"setlevel:VIP:{user.get('telegram_id')}")],
                        [InlineKeyboardButton(text="🤝 Partner", callback_data=f"setlevel:PARTNER:{user.get('telegram_id')}")],
                        [InlineKeyboardButton(text="❌ Cancel", callback_data=f"reject:{user.get('telegram_id')}")]
                    ]
                )
                await callback.message.answer(
                    f"📋 Approving user:\n"
                    f"👤 {user.get('first_name', '')} {user.get('last_name', '')}\n"
                    f"🆔 Telegram ID: {user.get('telegram_id')}\n"
                    f"🔗 Username: @{user.get('username', 'N/A')}\n\n"
                    "Please select the user level:",
                    reply_markup=level_selection_kb
                )
            except Exception as e:
                await callback.answer("❌ Something went wrong. Try again later.")
        await callback.answer()
    else:
        await callback.message.answer("🌟 All users have status", reply_markup=admin_info_kb)
        await callback.answer()
    await callback.message.delete()