from django.urls import path
from . import views

app_name = 'shop'

urlpatterns = [
    # Main pages
    path('', views.index, name='index'),
    path('catalog/', views.catalog, name='catalog'),
    path('cart/', views.cart, name='cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('favorites/', views.favorites, name='favorites'),
    path('account/', views.account, name='account'),
    path('settings/', views.settings, name='settings'),
    path('orders/', views.orders, name='orders'),
    path('order-confirmation/', views.order_confirmation, name='order_confirmation'),
    
    # Product detail page
    path('watch/<slug:slug>/', views.product_detail, name='product_detail'),
    
    # Category and brand filtering
    path('category/<slug:category_slug>/', views.catalog, name='category_catalog'),
    path('brand/<slug:brand_slug>/', views.catalog, name='brand_catalog'),
    
    # API endpoints for dynamic functionality
    path('api/add-to-cart/', views.add_to_cart, name='add_to_cart'),
    path('api/remove-from-cart/', views.remove_from_cart, name='remove_from_cart'),
    path('api/update-cart/', views.update_cart, name='update_cart'),
    path('api/add-to-favorites/', views.add_to_favorites, name='add_to_favorites'),
    path('api/remove-from-favorites/', views.remove_from_favorites, name='remove_from_favorites'),
]
