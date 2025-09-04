from django.contrib import admin
from django.utils.html import format_html
from .models import (
    Brand, Category, Product, ProductImage, WatchSpecification,
    JewelrySpecification, ProductCustomization, Review, Cart, CartItem,
    Order, OrderItem, HeroSection
)


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ('name', 'country', 'founded_year', 'is_active', 'show_on_homepage', 'created_at')
    list_filter = ('is_active', 'show_on_homepage', 'country', 'created_at')
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ('created_at', 'updated_at')
    list_editable = ('is_active', 'show_on_homepage')
    fieldsets = (
        (None, {
            'fields': ('name', 'slug', 'description', 'logo')
        }),
        ('Details', {
            'fields': ('founded_year', 'country', 'website')
        }),
        ('Status', {
            'fields': ('is_active', 'show_on_homepage')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent', 'is_active', 'sort_order', 'created_at')
    list_filter = ('is_active', 'parent', 'created_at')
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ('created_at', 'updated_at')
    list_editable = ('sort_order', 'is_active')
    
    fieldsets = (
        (None, {
            'fields': ('name', 'slug', 'description', 'image', 'parent')
        }),
        ('Settings', {
            'fields': ('is_active', 'sort_order')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1
    fields = ('image', 'alt_text', 'is_primary', 'sort_order')
    readonly_fields = ('created_at',)


class ProductCustomizationInline(admin.TabularInline):
    model = ProductCustomization
    extra = 1
    fields = ('customization_type', 'name', 'value', 'price_modifier', 'is_available', 'sort_order')
    list_editable = ('sort_order', 'is_available')


class WatchSpecificationInline(admin.StackedInline):
    model = WatchSpecification
    extra = 0
    fieldsets = (
        ('Case Specifications', {
            'fields': ('case_material', 'case_size', 'case_thickness', 'case_shape')
        }),
        ('Movement', {
            'fields': ('movement', 'movement_caliber', 'power_reserve', 'jewels', 'frequency')
        }),
        ('Dial & Display', {
            'fields': ('dial_color', 'dial_material', 'hands_style', 'markers_type', 'complications')
        }),
        ('Crystal & Protection', {
            'fields': ('crystal_type', 'water_resistance')
        }),
        ('Bracelet/Strap', {
            'fields': ('bracelet_material', 'bracelet_color', 'clasp_type', 'lug_width')
        }),
        ('Additional Features', {
            'fields': ('bezel_type', 'bezel_material', 'crown_type', 'certifications')
        }),
    )


class JewelrySpecificationInline(admin.StackedInline):
    model = JewelrySpecification
    extra = 0
    fieldsets = (
        ('Basic Information', {
            'fields': ('jewelry_type', 'metal_type', 'metal_purity', 'metal_weight')
        }),
        ('Gemstone Details', {
            'fields': ('has_gemstones', 'primary_gemstone', 'gemstone_carat', 'gemstone_clarity', 
                      'gemstone_color', 'gemstone_cut', 'stone_count')
        }),
        ('Dimensions', {
            'fields': ('length', 'width', 'thickness', 'ring_size', 'chain_length', 'pendant_dimensions')
        }),
        ('Design & Care', {
            'fields': ('style', 'finish', 'setting_type', 'care_instructions')
        }),
    )


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'brand', 'category', 'price', 'stock_status', 'rating_stars', 'is_active', 'is_featured', 'show_on_homepage', 'created_at')
    list_filter = ('brand', 'category', 'stock_status', 'is_active', 'is_featured', 'show_on_homepage', 'is_limited_edition', 'created_at')
    search_fields = ('name', 'description', 'sku', 'model_number')
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ('created_at', 'updated_at', 'sku')
    list_editable = ('price', 'stock_status', 'is_active', 'show_on_homepage')
    inlines = [ProductImageInline, ProductCustomizationInline, WatchSpecificationInline, JewelrySpecificationInline]
    
    fieldsets = (
        (None, {
            'fields': ('name', 'slug', 'brand', 'category', 'description', 'short_description', 'image', 'image_alt')
        }),
        ('Pricing', {
            'fields': ('price', 'original_price', 'cost_price')
        }),
        ('Inventory', {
            'fields': ('stock_status', 'stock_quantity', 'low_stock_threshold')
        }),
        ('Product Details', {
            'fields': ('sku', 'model_number', 'year_released')
        }),
        ('Ratings & Reviews', {
            'fields': ('rating_stars', 'review_count')
        }),
        ('SEO', {
            'fields': ('meta_title', 'meta_description', 'meta_keywords'),
            'classes': ('collapse',)
        }),
        ('Status', {
            'fields': ('is_active', 'is_featured', 'show_on_homepage', 'is_limited_edition')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('brand', 'category')


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ('product', 'alt_text', 'is_primary', 'sort_order', 'created_at')
    list_filter = ('is_primary', 'created_at')
    search_fields = ('product__name', 'alt_text')
    list_editable = ('is_primary', 'sort_order')
    readonly_fields = ('created_at',)


@admin.register(WatchSpecification)
class WatchSpecificationAdmin(admin.ModelAdmin):
    list_display = ('product', 'case_material', 'case_size', 'movement', 'water_resistance', 'crystal_type')
    list_filter = ('case_material', 'movement', 'crystal_type', 'case_material')
    search_fields = ('product__name', 'movement_caliber', 'case_material')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Case Specifications', {
            'fields': ('product', 'case_material', 'case_size', 'case_thickness', 'case_shape')
        }),
        ('Movement', {
            'fields': ('movement', 'movement_caliber', 'power_reserve', 'jewels', 'frequency')
        }),
        ('Dial & Display', {
            'fields': ('dial_color', 'dial_material', 'hands_style', 'markers_type', 'complications')
        }),
        ('Crystal & Protection', {
            'fields': ('crystal_type', 'water_resistance')
        }),
        ('Bracelet/Strap', {
            'fields': ('bracelet_material', 'bracelet_color', 'clasp_type', 'lug_width')
        }),
        ('Additional Features', {
            'fields': ('bezel_type', 'bezel_material', 'crown_type', 'certifications')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(JewelrySpecification)
class JewelrySpecificationAdmin(admin.ModelAdmin):
    list_display = ('product', 'jewelry_type', 'metal_type', 'has_gemstones', 'primary_gemstone', 'metal_weight')
    list_filter = ('jewelry_type', 'metal_type', 'has_gemstones', 'primary_gemstone')
    search_fields = ('product__name', 'metal_type', 'primary_gemstone')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('product', 'jewelry_type', 'metal_type', 'metal_purity', 'metal_weight')
        }),
        ('Gemstone Details', {
            'fields': ('has_gemstones', 'primary_gemstone', 'gemstone_carat', 'gemstone_clarity', 
                      'gemstone_color', 'gemstone_cut', 'stone_count')
        }),
        ('Dimensions', {
            'fields': ('length', 'width', 'thickness', 'ring_size', 'chain_length', 'pendant_dimensions')
        }),
        ('Design & Care', {
            'fields': ('style', 'finish', 'setting_type', 'care_instructions')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(ProductCustomization)
class ProductCustomizationAdmin(admin.ModelAdmin):
    list_display = ('product', 'customization_type', 'name', 'value', 'price_modifier', 'is_available', 'sort_order', 'created_at')
    list_filter = ('customization_type', 'is_available', 'created_at')
    search_fields = ('product__name', 'name', 'value')
    list_editable = ('price_modifier', 'is_available', 'sort_order')
    readonly_fields = ('created_at',)
    
    fieldsets = (
        (None, {
            'fields': ('product', 'customization_type', 'name', 'value', 'description')
        }),
        ('Pricing & Availability', {
            'fields': ('price_modifier', 'is_available', 'sort_order')
        }),
        ('Timestamps', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('product', 'customer_name', 'rating', 'title', 'is_verified_purchase', 'is_approved', 'created_at')
    list_filter = ('rating', 'is_verified_purchase', 'is_approved', 'created_at')
    search_fields = ('product__name', 'customer_name', 'title', 'comment')
    list_editable = ('is_approved',)
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        (None, {
            'fields': ('product', 'customer_name', 'customer_email', 'rating', 'title', 'comment')
        }),
        ('Status', {
            'fields': ('is_verified_purchase', 'is_approved', 'helpful_count')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('product')


class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0
    fields = ('product', 'quantity', 'unit_price', 'customization_price', 'total_price_display')
    readonly_fields = ('total_price_display', 'created_at', 'updated_at')
    
    def total_price_display(self, obj):
        if obj.pk:
            return f"${obj.total_price:.2f}"
        return "-"
    total_price_display.short_description = 'Total Price'


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('user_display', 'total_items_display', 'total_price_display', 'item_count_display', 'created_at', 'updated_at')
    list_filter = ('created_at', 'updated_at')
    search_fields = ('user__username', 'user__telegram_id', 'user__first_name', 'user__last_name')
    readonly_fields = ('total_items_display', 'total_price_display', 'item_count_display', 'created_at', 'updated_at')
    inlines = [CartItemInline]
    
    def user_display(self, obj):
        if obj.user.username:
            return obj.user.username
        elif hasattr(obj.user, 'telegram_id') and obj.user.telegram_id:
            return f"TG: {obj.user.telegram_id}"
        else:
            return f"User #{obj.user.id}"
    user_display.short_description = 'User'
    
    def total_items_display(self, obj):
        return obj.total_items
    total_items_display.short_description = 'Total Items'
    
    def total_price_display(self, obj):
        return f"${obj.total_price:.2f}"
    total_price_display.short_description = 'Total Price'
    
    def item_count_display(self, obj):
        return obj.item_count
    item_count_display.short_description = 'Different Items'


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('cart_user', 'product', 'quantity', 'unit_price', 'customization_price', 'total_price_display', 'created_at')
    list_filter = ('created_at', 'updated_at')
    search_fields = ('cart__user__username', 'cart__user__telegram_id', 'product__name')
    readonly_fields = ('total_price_display', 'customized_product_name_display', 'created_at', 'updated_at')
    
    fieldsets = (
        (None, {
            'fields': ('cart', 'product', 'quantity', 'unit_price')
        }),
        ('Customization', {
            'fields': ('customization_data', 'customization_price', 'customized_product_name_display')
        }),
        ('Totals', {
            'fields': ('total_price_display',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def cart_user(self, obj):
        if obj.cart.user.username:
            return obj.cart.user.username
        elif hasattr(obj.cart.user, 'telegram_id') and obj.cart.user.telegram_id:
            return f"TG: {obj.cart.user.telegram_id}"
        else:
            return f"User #{obj.cart.user.id}"
    cart_user.short_description = 'Cart User'
    
    def total_price_display(self, obj):
        return f"${obj.total_price:.2f}"
    total_price_display.short_description = 'Total Price'
    
    def customized_product_name_display(self, obj):
        return obj.customized_product_name
    customized_product_name_display.short_description = 'Product with Customizations'


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    fields = ('product', 'quantity', 'price', 'total_price_display', 'customization_summary')
    readonly_fields = ('total_price_display', 'customization_summary', 'created_at')
    
    def total_price_display(self, obj):
        if obj.pk:
            return f"${obj.total_price:.2f}"
        return "-"
    total_price_display.short_description = 'Total Price'
    
    def customization_summary(self, obj):
        if obj.customization_data:
            try:
                data = obj.customization_data if isinstance(obj.customization_data, dict) else {}
                return ', '.join(f'{k}: {v}' for k, v in data.items() if v)
            except:
                return "Invalid customization data"
        return "No customizations"
    customization_summary.short_description = 'Customizations'


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_number', 'user_display', 'status', 'total_amount', 'total_items', 'created_at')
    list_filter = ('status', 'created_at', 'updated_at')
    search_fields = ('order_number', 'user__username', 'user__telegram_id', 'customer_email', 'customer_first_name', 'customer_last_name')
    readonly_fields = ('order_number', 'created_at', 'updated_at')
    list_editable = ('status',)
    inlines = [OrderItemInline]
    
    fieldsets = (
        (None, {
            'fields': ('order_number', 'user', 'status')
        }),
        ('Order Details', {
            'fields': ('total_amount', 'total_items')
        }),
        ('Customer Information', {
            'fields': ('customer_email', 'customer_first_name', 'customer_last_name')
        }),
        ('Shipping Information', {
            'fields': ('shipping_first_name', 'shipping_last_name', 'shipping_address', 
                      'shipping_city', 'shipping_zip_code', 'shipping_country'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def user_display(self, obj):
        if obj.user.username:
            return obj.user.username
        elif hasattr(obj.user, 'telegram_id') and obj.user.telegram_id:
            return f"TG: {obj.user.telegram_id}"
        else:
            return f"User #{obj.user.id}"
    user_display.short_description = 'User'
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user')


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order_number', 'product', 'quantity', 'price', 'total_price_display', 'created_at')
    list_filter = ('created_at', 'order__status')
    search_fields = ('order__order_number', 'product__name')
    readonly_fields = ('total_price_display', 'customization_summary_display', 'created_at')
    
    fieldsets = (
        (None, {
            'fields': ('order', 'product', 'quantity', 'price')
        }),
        ('Customization', {
            'fields': ('customization_data', 'customization_summary_display')
        }),
        ('Totals', {
            'fields': ('total_price_display',)
        }),
        ('Timestamps', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )
    
    def order_number(self, obj):
        return obj.order.order_number
    order_number.short_description = 'Order Number'
    
    def total_price_display(self, obj):
        return f"${obj.total_price:.2f}"
    total_price_display.short_description = 'Total Price'
    
    def customization_summary_display(self, obj):
        if obj.customization_data:
            try:
                data = obj.customization_data if isinstance(obj.customization_data, dict) else {}
                return ', '.join(f'{k}: {v}' for k, v in data.items() if v)
            except:
                return "Invalid customization data"
        return "No customizations"
    customization_summary_display.short_description = 'Customizations'
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('order', 'product')


@admin.register(HeroSection)
class HeroSectionAdmin(admin.ModelAdmin):
    list_display = ('title', 'subtitle', 'button_text', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('title', 'subtitle')
    list_editable = ('is_active',)
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        (None, {
            'fields': ('title', 'subtitle', 'background_image')
        }),
        ('Button Settings', {
            'fields': ('button_text', 'button_url')
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def save_model(self, request, obj, form, change):
        # If setting this hero as active, deactivate all others
        if obj.is_active:
            HeroSection.objects.exclude(pk=obj.pk).update(is_active=False)
        super().save_model(request, obj, form, change)
