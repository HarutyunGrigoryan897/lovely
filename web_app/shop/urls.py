from django.urls import path
from . import views

app_name = 'shop'

urlpatterns = [
    # Main pages
    path('webapp_telegram/<str:page>/', views.webapptelegram, name="webapptelegram"),
    path('', views.index, name='index'),
    path('catalog/', views.catalog, name='catalog'),
    path('cart/', views.cart, name='cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('favorites/', views.favorites, name='favorites'),
    path('account/', views.account, name='account'),
    path('settings/', views.settings, name='settings'),
    path('orders/', views.orders, name='orders'),
    path('order-confirmation/', views.order_confirmation, name='order_confirmation'),
    path('order-confirmation/<int:order_id>/', views.order_confirmation, name='order_confirmation_with_id'),
    
    # Product detail page
    path('watch/<slug:slug>/', views.product_detail, name='product_detail'),
    
    # Category and brand filtering
    path('category/<slug:category_slug>/', views.catalog, name='category_catalog'),
    path('brand/<slug:brand_slug>/', views.catalog, name='brand_catalog'),
    
    # API endpoints for dynamic functionality
    path('api/add-to-cart/', views.add_to_cart_api, name='add_to_cart_api'),
    path('api/update-cart-item/', views.update_cart_item, name='update_cart_item'),
    path('api/remove-from-cart/', views.remove_from_cart, name='remove_from_cart'),
    path('api/get-cart/', views.get_cart_data, name='get_cart_data'),
    path('api/clear-cart/', views.clear_cart, name='clear_cart'),
    path('api/create-order/', views.create_order_from_cart, name='create_order_from_cart'),
    path('process-checkout/', views.process_checkout, name='process_checkout'),
    path('api/add-to-favorites/', views.add_to_favorites, name='add_to_favorites'),
    path('api/remove-from-favorites/', views.remove_from_favorites, name='remove_from_favorites'),
    
    # Shipping address management
    path('api/shipping-addresses/', views.get_shipping_addresses, name='get_shipping_addresses'),
    path('api/shipping-addresses/add/', views.add_shipping_address, name='add_shipping_address'),
    path('api/shipping-addresses/<int:address_id>/update/', views.update_shipping_address, name='update_shipping_address'),
    path('api/shipping-addresses/<int:address_id>/delete/', views.delete_shipping_address, name='delete_shipping_address'),
    path('api/shipping-addresses/<int:address_id>/set-default/', views.set_default_address, name='set_default_address'),
    
    # Product pricing and details
    path('api/product/<slug:product_slug>/calculate-price/', views.calculate_product_price, name='calculate_product_price'),
    path('api/product/<slug:product_slug>/details/', views.get_product_details, name='get_product_details'),
    path('api/get-diamond-prices/', views.get_diamond_prices, name='get_diamond_prices'),
    
    # Order management (for Telegram bot)
    path('api/order/<int:order_id>/update-status/', views.update_order_status, name='update_order_status'),
    path('api/order/<int:order_id>/details/', views.get_order_details, name='get_order_details'),
]
