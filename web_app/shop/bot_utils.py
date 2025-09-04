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
    for item in order.items.all():
        # Base item info
        item_text = f"• {item.product.name} x{item.quantity} - ${item.price * item.quantity}"
        
        # Add customization details if available
        if item.customization_data:
            try:
                # Handle customization data
                customization_data = item.customization_data if isinstance(item.customization_data, dict) else {}
                if customization_data:
                    customizations = []
                    for key, value in customization_data.items():
                        if value and value != 'None' and str(value).strip():
                            # Format customization display
                            if key == 'band_color':
                                customizations.append(f"Band: {value}")
                            elif key == 'dial_color':
                                customizations.append(f"Dial: {value}")
                            elif key == 'case_material':
                                customizations.append(f"Case: {value}")
                            elif key == 'engraving':
                                customizations.append(f"Engraving: '{value}'")
                            elif key == 'size':
                                customizations.append(f"Size: {value}")
                            elif key == 'length':
                                customizations.append(f"Length: {value}")
                            elif key == 'metal_type':
                                customizations.append(f"Metal: {value}")
                            elif key == 'gemstone':
                                customizations.append(f"Gemstone: {value}")
                            else:
                                # Generic formatting for any other customizations
                                formatted_key = key.replace('_', ' ').title()
                                customizations.append(f"{formatted_key}: {value}")
                    
                    if customizations:
                        item_text += f"\n  └ Customizations: {', '.join(customizations)}"
            except (TypeError, AttributeError, ValueError) as e:
                # If there's an error processing customization data, just note it
                item_text += f"\n  └ Custom options selected"
                print(f"Error processing customization data for item {item.id}: {e}")
        
        order_items.append(item_text)
    
    items_text = "\n".join(order_items) if order_items else "No items"
    
    text = (
        f"📦 New order created!\n\n"
        f"Order #: {order.order_number}\n"
        f"Customer: {order.customer_first_name} {order.customer_last_name}\n"
        f"Email: {order.customer_email}\n\n"
        f"Items:\n{items_text}\n\n"
        f"Shipping Address:\n"
        f"{order.shipping_first_name} {order.shipping_last_name}\n"
        f"{order.shipping_address}\n"
        f"{order.shipping_city}, {order.shipping_zip_code}\n"
        f"{order.shipping_country}\n\n"
        f"Total: ${order.total_amount}\n"
        f"Items: {order.total_items}"
    )

    keyboard = {
        "inline_keyboard": [
            [
                {"text": "✅ Approve", "callback_data": f"order_approve:{order.id}"},
                {"text": "❌ Reject", "callback_data": f"order_reject:{order.id}"}
            ]
        ]
    }

    for admin_id in admins_list:
        url = f"https://api.telegram.org/bot{token}/sendMessage"
        payload = {
            "chat_id": admin_id,
            "text": text,
            "reply_markup": json.dumps(keyboard)
        }
        try:
            response = requests.post(url, data=payload, timeout=5)
            response.raise_for_status()
        except requests.RequestException as e:
            print(f"Failed to send Telegram message to {admin_id}: {e}")
