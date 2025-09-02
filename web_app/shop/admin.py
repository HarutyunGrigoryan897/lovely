from django.contrib import admin
from django.utils.html import format_html
from .models import (
    Brand, Category, Product, ProductImage, WatchSpecification,
    JewelrySpecification, ProductCustomization, Review
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
    list_display = ('product', 'case_material', 'case_size', 'movement', 'water_resistance')
    list_filter = ('case_material', 'movement', 'crystal_type')
    search_fields = ('product__name', 'movement_caliber', 'case_material')
    readonly_fields = ('created_at', 'updated_at')


@admin.register(JewelrySpecification)
class JewelrySpecificationAdmin(admin.ModelAdmin):
    list_display = ('product', 'jewelry_type', 'metal_type', 'has_gemstones', 'primary_gemstone')
    list_filter = ('jewelry_type', 'metal_type', 'has_gemstones', 'primary_gemstone')
    search_fields = ('product__name', 'metal_type', 'primary_gemstone')
    readonly_fields = ('created_at', 'updated_at')


@admin.register(ProductCustomization)
class ProductCustomizationAdmin(admin.ModelAdmin):
    list_display = ('product', 'customization_type', 'name', 'value', 'price_modifier', 'is_available', 'sort_order')
    list_filter = ('customization_type', 'is_available')
    search_fields = ('product__name', 'name', 'value')
    list_editable = ('price_modifier', 'is_available', 'sort_order')


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
