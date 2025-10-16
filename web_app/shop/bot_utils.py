from decouple import config
from django.contrib.auth import get_user_model

import requests
import json

def send_order_message(order):
    User = get_user_model()
    # Filter out admins without telegram_id or with None/empty/invalid telegram_id
    admins_list = list(User.objects.filter(
        is_superuser=True, 
        telegram_id__isnull=False,
        telegram_id__gt=0  # Ensure telegram_id is a positive number
    ).values_list("telegram_id", flat=True))
    
    # If no admins have telegram_id, skip sending
    if not admins_list:
        print("No admin users with valid telegram_id found")
        return

    token = config("BOT_TOKEN")
    
    # Build order details
    order_items = []
    for idx, item in enumerate(order.items.all(), 1):
        # Format price with thousand separators
        item_total = float(item.price * item.quantity)
        formatted_price = f"{item_total:,.2f}"
        
        # Get product details
        product = item.product
        
        # Base item info with better formatting
        item_text = f"{idx}. 💎 {product.name}\n"
        item_text += f"   🏷 Brand: {product.brand.name}\n"
        item_text += f"   📦 Quantity: {item.quantity}\n"
        item_text += f"   💵 Unit Price: ${float(item.price):,.2f}\n"
        item_text += f"   💰 Subtotal: ${formatted_price}"
        
        # Add product specifications
        specs = []
        if product.sku:
            specs.append(f"📋 SKU: {product.sku}")
        if product.model_number:
            specs.append(f"🔢 Model: {product.model_number}")
        if product.year_released:
            specs.append(f"📅 Year: {product.year_released}")
        if product.gold_weight_grams and product.gold_weight_grams > 0:
            specs.append(f"⚖️ Gold Weight: {product.gold_weight_grams}g")
        if product.has_diamonds:
            diamond_info = f"💎 Diamonds: {product.get_diamond_type_display() if product.diamond_type else 'Yes'}"
            specs.append(diamond_info)
        if product.stock_status:
            specs.append(f"📊 Stock: {product.get_stock_status_display()}")
        if product.is_limited_edition:
            specs.append(f"⭐ Limited Edition")
        
        # Add watch specifications if available
        if hasattr(product, 'watch_specs') and product.watch_specs:
            watch = product.watch_specs
            if watch.case_material:
                specs.append(f"🔧 Case: {watch.get_case_material_display()}, {watch.case_size}")
            if watch.movement:
                specs.append(f"⚙️ Movement: {watch.get_movement_display()}")
            if watch.dial_color:
                specs.append(f"🎨 Dial: {watch.dial_color}")
            if watch.water_resistance:
                specs.append(f"💧 Water Resistance: {watch.water_resistance}")
            if watch.crystal_type:
                specs.append(f"💎 Crystal: {watch.get_crystal_type_display()}")
            if watch.bracelet_material:
                specs.append(f"⛓ Bracelet: {watch.bracelet_material}")
        
        if specs:
            item_text += f"\n   📝 Specifications:\n"
            for spec in specs:
                item_text += f"      • {spec}\n"
            item_text = item_text.rstrip('\n')
        
        # Add customization details if available
        if item.customization_data:
            try:
                # Handle customization data
                customization_data = item.customization_data if isinstance(item.customization_data, dict) else {}
                if customization_data:
                    customizations = []
                    for key, value in customization_data.items():
                        if value and value != 'None' and str(value).strip():
                            # Format customization display with emojis
                            if key == 'band_color':
                                customizations.append(f"🎨 Band: {value}")
                            elif key == 'dial_color':
                                customizations.append(f"⌚ Dial: {value}")
                            elif key == 'case_material':
                                customizations.append(f"🔧 Case: {value}")
                            elif key == 'engraving':
                                customizations.append(f"✍️ Engraving: '{value}'")
                            elif key == 'size':
                                customizations.append(f"📏 Size: {value}")
                            elif key == 'length':
                                customizations.append(f"📐 Length: {value}")
                            elif key == 'metal_type':
                                customizations.append(f"⚜️ Metal: {value}")
                            elif key == 'gemstone':
                                customizations.append(f"💎 Gemstone: {value}")
                            elif key == 'diamond_type':
                                customizations.append(f"💎 Diamond Type: {value}")
                            elif key.startswith('diamonds_'):
                                # Handle diamond quantity selections
                                size_name = key.replace('diamonds_', '').replace('_', ' ').title()
                                customizations.append(f"💎 Diamonds ({size_name}): {value} pcs")
                            else:
                                # Generic formatting for any other customizations
                                formatted_key = key.replace('_', ' ').title()
                                customizations.append(f"✨ {formatted_key}: {value}")
                    
                    if customizations:
                        item_text += f"\n   🎯 Customizations:\n"
                        for custom in customizations:
                            item_text += f"      • {custom}\n"
                        item_text = item_text.rstrip('\n')  # Remove last newline
            except (TypeError, AttributeError, ValueError) as e:
                # If there's an error processing customization data, just note it
                item_text += f"\n   ℹ️ Custom options selected"
                print(f"Error processing customization data for item {item.id}: {e}")
        
        order_items.append(item_text)
    
    items_text = "\n\n".join(order_items) if order_items else "No items"
    
    # Format total amount with thousand separators
    formatted_total = f"{float(order.total_amount):,.2f}"
    
    # Get user information and level
    user = order.user
    user_level_info = ""
    if hasattr(user, 'user_level') and user.user_level:
        user_level_info = f"\n💼 User Level: {user.user_level.get_name_display()} (×{user.user_level.multiplier})"
    
    # Get order status display
    status_display = order.get_status_display() if hasattr(order, 'get_status_display') else order.status
    
    text = (
        f"🎉 ═══════════════════════════\n"
        f"        🆕 NEW ORDER RECEIVED\n"
        f"═══════════════════════════\n\n"
        f"📋 ORDER DETAILS\n"
        f"━━━━━━━━━━━━━━━━━━━━━━\n"
        f"🔖 Order Number: #{order.order_number}\n"
        f"📅 Date: {order.created_at.strftime('%B %d, %Y at %H:%M')}\n"
        f"✨ Status: {status_display.title()}\n\n"
        f"👤 CUSTOMER INFORMATION\n"
        f"━━━━━━━━━━━━━━━━━━━━━━\n"
        f"👨‍💼 Name: {order.customer_first_name} {order.customer_last_name}\n"
        f"📧 Email: {order.customer_email}\n"
        f"🆔 User ID: {user.telegram_id or user.username or user.id}{user_level_info}\n\n"
        f"🛍 ORDERED ITEMS ({order.total_items} item{'s' if order.total_items > 1 else ''})\n"
        f"━━━━━━━━━━━━━━━━━━━━━━\n"
        f"{items_text}\n\n"
        f"📍 SHIPPING ADDRESS\n"
        f"━━━━━━━━━━━━━━━━━━━━━━\n"
        f"👤 Recipient: {order.shipping_first_name} {order.shipping_last_name}\n"
        f"🏠 Address: {order.shipping_address}\n"
        f"🏙 City: {order.shipping_city}\n"
        f"📮 Postal Code: {order.shipping_zip_code}\n"
        f"🌍 Country: {order.shipping_country}\n\n"
        f"💰 PAYMENT SUMMARY\n"
        f"━━━━━━━━━━━━━━━━━━━━━━\n"
        f"� Total Items: {order.total_items}\n"
        f"💵 Total Amount: ${formatted_total}\n\n"
        f"═══════════════════════════\n"
        f"⚡ Please review and take action below"
    )

    keyboard = {
        "inline_keyboard": [
            [
                {"text": "✅ Accept Order", "callback_data": f"order_approve:{order.id}"},
                {"text": "❌ Decline Order", "callback_data": f"order_reject:{order.id}"}
            ],
            [
                {"text": "📋 View Order Details", "callback_data": f"order_view:{order.id}"}
            ]
        ]
    }

    for admin_id in admins_list:
        url = f"https://api.telegram.org/bot{token}/sendMessage"
        payload = {
            "chat_id": admin_id,
            "text": text,
            "reply_markup": json.dumps(keyboard),
            "parse_mode": "HTML"  # Enable HTML formatting for better display
        }
        try:
            response = requests.post(url, data=payload, timeout=5)
            response.raise_for_status()
        except requests.RequestException as e:
            print(f"Failed to send Telegram message to {admin_id}: {e}")
