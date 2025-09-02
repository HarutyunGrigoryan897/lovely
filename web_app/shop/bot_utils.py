from decouple import config
from django.contrib.auth import get_user_model

import requests
import json

def send_order_message(order):
    User = get_user_model()
    admins_list = list(User.objects.filter(is_superuser=True).values_list("telegram_id", flat=True))

    token = config("BOT_TOKEN")
    text = (
        f"📦 New order created!\n\n"
        f"Order ID: {order.id}\n"
        f"User: {order.user.first_name} @{order.user.username if order.user.username else ''}\n"
        f"Total: {order.total_price} $"
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
