from rest_framework import serializers
from authorization.models import CustomUser
from shop.models import OrderItem, Order

class CustomUserSerializer(serializers.ModelSerializer):
    telegram_id = serializers.IntegerField(required=True)
    username = serializers.CharField(required=False, allow_blank=True)
    first_name = serializers.CharField(required=False, allow_blank=True)
    last_name = serializers.CharField(required=False, allow_blank=True)

    class Meta:
        model = CustomUser
        fields = ["telegram_id", "username", "first_name", "last_name", "approved"]
        validators = []

    def create(self, validated_data):
        telegram_id = validated_data.get("telegram_id")
        user, created = CustomUser.objects.get_or_create(
            telegram_id=telegram_id,
            defaults={
                "username": validated_data.get("username") or "",
                "first_name": validated_data.get("first_name") or "",
                "last_name": validated_data.get("last_name") or "",
                "approved": False,
            }
        )

        if not created:
            # Update fields if provided
            if validated_data.get("username") is not None:
                user.username = validated_data.get("username")
            if validated_data.get("first_name") is not None:
                user.first_name = validated_data.get("first_name")
            if validated_data.get("last_name") is not None:
                user.last_name = validated_data.get("last_name")
            user.save()

        return user


class CustomUserInfoSerializer(serializers.ModelSerializer):
    date_joined = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = ["telegram_id", "username", "first_name", "last_name", "approved", "date_joined"]

    def get_date_joined(self, obj):
        return obj.date_joined.strftime("%d %B %Y")
    
class OrderItemSerializer(serializers.ModelSerializer):
    """Serialize each item in the order"""
    product_name = serializers.CharField(source="product.name", read_only=True)
    brand_name = serializers.CharField(source="product.brand.name", read_only=True)
    subtotal = serializers.SerializerMethodField()

    class Meta:
        model = OrderItem
        fields = [
            "id", "product_name", "brand_name", "quantity", "price",
            "subtotal", "customization_data"
        ]

    def get_subtotal(self, obj):
        return float(obj.price * obj.quantity)


class OrderSerializer(serializers.ModelSerializer):
    """Full order serializer with formatted Telegram-style text output"""
    items = OrderItemSerializer(many=True, read_only=True)
    formatted_text = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = [
            "id", "order_number", "status", "total_amount", "total_items",
            "customer_email", "customer_first_name", "customer_last_name",
            "shipping_first_name", "shipping_last_name", "shipping_address",
            "shipping_city", "shipping_zip_code", "shipping_country",
            "created_at", "formatted_text", "items"
        ]

    def get_formatted_text(self, order):
        """Return a formatted text block (Telegram message style)"""
        order_items = []
        for idx, item in enumerate(order.items.all(), 1):
            item_total = float(item.price * item.quantity)
            formatted_price = f"{item_total:,.2f}"
            product = item.product

            item_text = f"{idx}. 💎 {product.name}\n"
            if getattr(product, "brand", None):
                item_text += f"   🏷 Brand: {product.brand.name}\n"
            item_text += (
                f"   📦 Quantity: {item.quantity}\n"
                f"   💵 Unit Price: ${float(item.price):,.2f}\n"
                f"   💰 Subtotal: ${formatted_price}"
            )

            # --- SPECIFICATIONS ---
            specs = []
            if getattr(product, "sku", None):
                specs.append(f"📋 SKU: {product.sku}")
            if getattr(product, "model_number", None):
                specs.append(f"🔢 Model: {product.model_number}")
            if getattr(product, "year_released", None):
                specs.append(f"📅 Year: {product.year_released}")
            if getattr(product, "gold_weight_grams", 0):
                specs.append(f"⚖️ Gold Weight: {product.gold_weight_grams}g")
            if getattr(product, "has_diamonds", False):
                diamond_info = (
                    f"💎 Diamonds: {product.get_diamond_type_display()}"
                    if getattr(product, "diamond_type", None)
                    else "💎 Diamonds: Yes"
                )
                specs.append(diamond_info)
            if getattr(product, "stock_status", None):
                specs.append(f"📊 Stock: {product.get_stock_status_display()}")
            if getattr(product, "is_limited_edition", False):
                specs.append(f"⭐ Limited Edition")

            if hasattr(product, "watch_specs") and product.watch_specs:
                watch = product.watch_specs
                # if getattr(watch, "case_material", None):
                #     specs.append(f"🔧 Case: {watch.get_case_material_display()}, {watch.case_size}")
                if getattr(watch, "movement", None):
                    specs.append(f"⚙️ Movement: {watch.get_movement_display()}")
                # if getattr(watch, "dial_color", None):
                #     specs.append(f"🎨 Dial: {watch.dial_color}")
                # if getattr(watch, "water_resistance", None):
                #     specs.append(f"💧 Water Resistance: {watch.water_resistance}")
                # if getattr(watch, "crystal_type", None):
                #     specs.append(f"💎 Crystal: {watch.get_crystal_type_display()}")
                # if getattr(watch, "bracelet_material", None):
                #     specs.append(f"⛓ Bracelet: {watch.bracelet_material}")

            if specs:
                item_text += "\n   📝 Specifications:\n"
                for spec in specs:
                    item_text += f"      • {spec}\n"
                item_text = item_text.rstrip("\n")

            # --- CUSTOMIZATIONS ---
            if item.customization_data:
                try:
                    data = (
                        item.customization_data
                        if isinstance(item.customization_data, dict)
                        else {}
                    )
                    customizations = []
                    for key, value in data.items():
                        if not value or str(value).strip() in ["None", ""]:
                            continue
                        emoji_map = {
                            # "band_color": "🎨 Band",
                            # "dial_color": "⌚ Dial",
                            # "case_material": "🔧 Case",
                            "engraving": "✍️ Engraving",
                            "size": "📏 Size",
                            "length": "📐 Length",
                            # "metal_type": "⚜️ Metal",
                            # "gemstone": "💎 Gemstone",
                            "diamond_type": "💎 Diamond Type",
                        }
                        if key.startswith("diamonds_"):
                            size_name = key.replace("diamonds_", "").replace("_", " ").title()
                            customizations.append(f"💎 Diamonds ({size_name}): {value} pcs")
                        else:
                            label = emoji_map.get(key, f"✨ {key.replace('_', ' ').title()}")
                            customizations.append(f"{label}: {value}")

                    if customizations:
                        item_text += "\n   🎯 Customizations:\n"
                        for c in customizations:
                            item_text += f"      • {c}\n"
                        item_text = item_text.rstrip("\n")
                except Exception as e:
                    item_text += "\n   ℹ️ Custom options selected"

            order_items.append(item_text)

        items_text = "\n\n".join(order_items) if order_items else "No items"
        formatted_total = f"{float(order.total_amount):,.2f}"

        # USER INFO
        user = order.user
        user_level_info = ""
        if getattr(user, "user_level", None):
            user_level_info = (
                f"\n💼 User Level: {user.user_level.name} (×{user.user_level.multiplier})"
            )

        status_display = order.get_status_display() if hasattr(order, "get_status_display") else order.status

        # FINAL MESSAGE TEXT
        return (
            f"══════════════════\n"
            f"        🆕 ORDER\n"
            f"══════════════════\n\n"
            f"📋 ORDER DETAILS\n"
            f"━━━━━━━━━━━━━━━━━━\n"
            f"🔖 Order Number: #{order.order_number}\n"
            f"📅 Date: {order.created_at.strftime('%B %d, %Y at %H:%M')}\n"
            f"✨ Status: {status_display.title()}\n\n"
            f"👤 CUSTOMER INFORMATION\n"
            f"━━━━━━━━━━━━━━━━━━\n"
            f"👨‍💼 Name: {order.customer_first_name} {order.customer_last_name}\n"
            f"📧 Email: {order.customer_email}\n"
            f"🆔 User ID: {user.telegram_id or user.username or user.id}{user_level_info}\n\n"
            f"🛍 ORDERED ITEMS ({order.total_items} item{'s' if order.total_items > 1 else ''})\n"
            f"━━━━━━━━━━━━━━━━━━\n"
            f"{items_text}\n\n"
            f"📍 SHIPPING ADDRESS\n"
            f"━━━━━━━━━━━━━━━━━━\n"
            f"👤 Recipient: {order.shipping_first_name} {order.shipping_last_name}\n"
            f"🏠 Address: {order.shipping_address}\n"
            f"🏙 City: {order.shipping_city}\n"
            f"📮 Postal Code: {order.shipping_zip_code}\n"
            f"🌍 Country: {order.shipping_country}\n\n"
            f"💰 PAYMENT SUMMARY\n"
            f"━━━━━━━━━━━━━━━━━━\n"
            f"📦 Total Items: {order.total_items}\n"
            f"💵 Total Amount: ${formatted_total}\n\n"
            f"══════════════════\n"
            f"⚡ Please review and take action below"
        )


class ShippingSerializer(serializers.ModelSerializer):
    """Full order serializer with formatted Telegram-style text output"""
    items = OrderItemSerializer(many=True, read_only=True)
    formatted_text = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = [
            "id", "order_number", "status", "total_amount", "total_items",
            "customer_email", "customer_first_name", "customer_last_name",
            "shipping_first_name", "shipping_last_name", "shipping_address",
            "shipping_city", "shipping_zip_code", "shipping_country",
            "created_at", "formatted_text", "items"
        ]

    def get_formatted_text(self, order):
        """Return a formatted text block (Telegram message style)"""
        order_items = []
        for idx, item in enumerate(order.items.all(), 1):
            item_total = float(item.price * item.quantity)
            formatted_price = f"{item_total:,.2f}"
            product = item.product

            item_text = f"{idx}. 💎 {product.name}\n"
            if getattr(product, "brand", None):
                item_text += f"   🏷 Brand: {product.brand.name}\n"
            item_text += (
                f"   📦 Quantity: {item.quantity}\n"
                f"   💵 Unit Price: ${float(item.price):,.2f}\n"
                f"   💰 Subtotal: ${formatted_price}"
            )

            # --- SPECIFICATIONS ---
            specs = []
            if getattr(product, "sku", None):
                specs.append(f"📋 SKU: {product.sku}")
            if getattr(product, "model_number", None):
                specs.append(f"🔢 Model: {product.model_number}")
            if getattr(product, "year_released", None):
                specs.append(f"📅 Year: {product.year_released}")
            if getattr(product, "gold_weight_grams", 0):
                specs.append(f"⚖️ Gold Weight: {product.gold_weight_grams}g")
            if getattr(product, "has_diamonds", False):
                diamond_info = (
                    f"💎 Diamonds: {product.get_diamond_type_display()}"
                    if getattr(product, "diamond_type", None)
                    else "💎 Diamonds: Yes"
                )
                specs.append(diamond_info)
            if getattr(product, "stock_status", None):
                specs.append(f"📊 Stock: {product.get_stock_status_display()}")
            if getattr(product, "is_limited_edition", False):
                specs.append(f"⭐ Limited Edition")

            if hasattr(product, "watch_specs") and product.watch_specs:
                watch = product.watch_specs
                # if getattr(watch, "case_material", None):
                #     specs.append(f"🔧 Case: {watch.get_case_material_display()}, {watch.case_size}")
                if getattr(watch, "movement", None):
                    specs.append(f"⚙️ Movement: {watch.get_movement_display()}")
                # if getattr(watch, "dial_color", None):
                #     specs.append(f"🎨 Dial: {watch.dial_color}")
                # if getattr(watch, "water_resistance", None):
                #     specs.append(f"💧 Water Resistance: {watch.water_resistance}")
                # if getattr(watch, "crystal_type", None):
                #     specs.append(f"💎 Crystal: {watch.get_crystal_type_display()}")
                # if getattr(watch, "bracelet_material", None):
                #     specs.append(f"⛓ Bracelet: {watch.bracelet_material}")

            if specs:
                item_text += "\n   📝 Specifications:\n"
                for spec in specs:
                    item_text += f"      • {spec}\n"
                item_text = item_text.rstrip("\n")

            # --- CUSTOMIZATIONS ---
            if item.customization_data:
                try:
                    data = (
                        item.customization_data
                        if isinstance(item.customization_data, dict)
                        else {}
                    )
                    customizations = []
                    for key, value in data.items():
                        if not value or str(value).strip() in ["None", ""]:
                            continue
                        emoji_map = {
                            # "band_color": "🎨 Band",
                            # "dial_color": "⌚ Dial",
                            # "case_material": "🔧 Case",
                            "engraving": "✍️ Engraving",
                            "size": "📏 Size",
                            "length": "📐 Length",
                            # "metal_type": "⚜️ Metal",
                            # "gemstone": "💎 Gemstone",
                            "diamond_type": "💎 Diamond Type",
                        }
                        if key.startswith("diamonds_"):
                            size_name = key.replace("diamonds_", "").replace("_", " ").title()
                            customizations.append(f"💎 Diamonds ({size_name}): {value} pcs")
                        else:
                            label = emoji_map.get(key, f"✨ {key.replace('_', ' ').title()}")
                            customizations.append(f"{label}: {value}")

                    if customizations:
                        item_text += "\n   🎯 Customizations:\n"
                        for c in customizations:
                            item_text += f"      • {c}\n"
                        item_text = item_text.rstrip("\n")
                except Exception as e:
                    item_text += "\n   ℹ️ Custom options selected"

            order_items.append(item_text)

        items_text = "\n\n".join(order_items) if order_items else "No items"
        formatted_total = f"{float(order.total_amount):,.2f}"

        # USER INFO
        user = order.user
        user_level_info = ""
        if getattr(user, "user_level", None):
            user_level_info = (
                f"\n💼 User Level: {user.user_level.name} (×{user.user_level.multiplier})"
            )

        status_display = order.get_status_display() if hasattr(order, "get_status_display") else order.status

        # FINAL MESSAGE TEXT
        return (
            f"══════════════════\n"
            f"        🆕 ORDER\n"
            f"══════════════════\n\n"
            f"📋 ORDER DETAILS\n"
            f"━━━━━━━━━━━━━━━━━━\n"
            f"🔖 Order Number: #{order.order_number}\n"
            f"📅 Date: {order.created_at.strftime('%B %d, %Y at %H:%M')}\n"
            f"✨ Status: {status_display.title()}\n\n"
            f"👤 CUSTOMER INFORMATION\n"
            f"━━━━━━━━━━━━━━━━━━\n"
            f"👨‍💼 Name: {order.customer_first_name} {order.customer_last_name}\n"
            f"📧 Email: {order.customer_email}\n"
            f"🆔 User ID: {user.telegram_id or user.username or user.id}{user_level_info}\n\n"
            f"🛍 ORDERED ITEMS ({order.total_items} item{'s' if order.total_items > 1 else ''})\n"
            f"━━━━━━━━━━━━━━━━━━\n"
            f"📍 SHIPPING ADDRESS\n"
            f"━━━━━━━━━━━━━━━━━━\n"
            f"👤 Recipient: {order.shipping_first_name} {order.shipping_last_name}\n"
            f"🏠 Address: {order.shipping_address}\n"
            f"🏙 City: {order.shipping_city}\n"
            f"📮 Postal Code: {order.shipping_zip_code}\n"
            f"🌍 Country: {order.shipping_country}\n\n"
            f"💰 PAYMENT SUMMARY\n"
            f"━━━━━━━━━━━━━━━━━━\n"
            f"📦 Total Items: {order.total_items}\n"
            f"💵 Total Amount: ${formatted_total}\n\n"
            f"══════════════════\n"
            f"⚡ Please review and take action below"
        )