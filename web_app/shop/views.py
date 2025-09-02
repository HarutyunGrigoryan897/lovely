from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Product, Category, Brand, WatchSpecification, JewelrySpecification, ProductCustomization


def index(request):
    """Homepage with featured products"""
    featured_products = Product.objects.filter(
        is_active=True, 
        show_on_homepage=True
    ).select_related('brand', 'category')[:8]
    categories = Category.objects.filter(is_active=True, parent=None).order_by('sort_order')
    brands = Brand.objects.filter(is_active=True, show_on_homepage=True)[:6]
    
    context = {
        'featured_products': featured_products,
        'categories': categories,
        'brands': brands,
    }
    return render(request, 'index.html', context)


def catalog(request, category_slug=None, brand_slug=None):
    """Product catalog with filtering"""
    products = Product.objects.filter(is_active=True).select_related('brand', 'category')
    
    # Filter by category
    selected_category = None
    if category_slug:
        selected_category = get_object_or_404(Category, slug=category_slug, is_active=True)
        products = products.filter(category=selected_category)
    
    # Filter by brand (support both URL parameter and GET parameter)
    selected_brand = None
    if brand_slug:
        selected_brand = get_object_or_404(Brand, slug=brand_slug, is_active=True)
        products = products.filter(brand=selected_brand)
    else:
        # Check for brand filter in GET parameters (from homepage links)
        brand_param = request.GET.get('brand')
        if brand_param:
            try:
                selected_brand = Brand.objects.get(slug=brand_param, is_active=True)
                products = products.filter(brand=selected_brand)
            except Brand.DoesNotExist:
                pass
    
    # Search functionality
    search_query = request.GET.get('search', '')
    if search_query:
        products = products.filter(
            Q(name__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(brand__name__icontains=search_query)
        )
    
    # Sorting
    sort_by = request.GET.get('sort', 'name')
    if sort_by == 'price_low':
        products = products.order_by('price')
    elif sort_by == 'price_high':
        products = products.order_by('-price')
    elif sort_by == 'newest':
        products = products.order_by('-created_at')
    elif sort_by == 'rating':
        products = products.order_by('-rating_stars')
    else:
        products = products.order_by('name')
    
    # Pagination
    paginator = Paginator(products, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Get all categories and brands for filtering
    categories = Category.objects.filter(is_active=True, parent=None).order_by('sort_order')
    brands = Brand.objects.filter(is_active=True).order_by('name')
    
    context = {
        'page_obj': page_obj,
        'products': page_obj.object_list,
        'categories': categories,
        'brands': brands,
        'selected_category': selected_category,
        'selected_brand': selected_brand,
        'search_query': search_query,
        'sort_by': sort_by,
    }
    return render(request, 'catalog.html', context)


def product_detail(request, slug):
    """Individual product detail page"""
    product = get_object_or_404(Product, slug=slug, is_active=True)
    
    # Get specifications based on product type
    watch_specs = None
    jewelry_specs = None
    
    try:
        watch_specs = product.watch_specs
    except WatchSpecification.DoesNotExist:
        pass
    
    try:
        jewelry_specs = product.jewelry_specs
    except JewelrySpecification.DoesNotExist:
        pass
    
    # Get customization options grouped by type
    customizations = ProductCustomization.objects.filter(product=product, is_available=True).order_by('customization_type', 'sort_order')
    customization_groups = {}
    for customization in customizations:
        if customization.customization_type not in customization_groups:
            customization_groups[customization.customization_type] = []
        customization_groups[customization.customization_type].append(customization)
    
    # Get related products
    related_products = Product.objects.filter(
        category=product.category,
        is_active=True
    ).exclude(id=product.id).select_related('brand', 'category')[:4]
    
    context = {
        'product': product,
        'watch_specs': watch_specs,
        'jewelry_specs': jewelry_specs,
        'customization_groups': customization_groups,
        'related_products': related_products,
    }
    return render(request, 'watch.html', context)


def cart(request):
    """Shopping cart page"""
    context = {}
    return render(request, 'cart.html', context)


def checkout(request):
    """Checkout page"""
    context = {}
    return render(request, 'checkout.html', context)


def favorites(request):
    """Favorites/Wishlist page"""
    context = {}
    return render(request, 'favorites.html', context)


def account(request):
    """User account page"""
    context = {
        'user': request.user if request.user.is_authenticated else None,
        'is_telegram_user': bool(getattr(request.user, 'telegram_id', None)) if request.user.is_authenticated else False,
    }
    return render(request, 'account.html', context)


def settings(request):
    """User settings page"""
    context = {}
    return render(request, 'settings.html', context)


def orders(request):
    """User orders page"""
    context = {}
    return render(request, 'orders.html', context)


def order_confirmation(request):
    """Order confirmation page"""
    context = {}
    return render(request, 'order-confirmation.html', context)


# API Views for AJAX functionality
def add_to_cart(request):
    """Add item to cart via AJAX"""
    if request.method == 'POST':
        # Implementation depends on your cart system (session, database, etc.)
        return JsonResponse({'success': True, 'message': 'Product added to cart'})
    return JsonResponse({'success': False, 'message': 'Invalid request'})


def remove_from_cart(request):
    """Remove item from cart via AJAX"""
    if request.method == 'POST':
        # Implementation depends on your cart system
        return JsonResponse({'success': True, 'message': 'Product removed from cart'})
    return JsonResponse({'success': False, 'message': 'Invalid request'})


def update_cart(request):
    """Update cart item quantity via AJAX"""
    if request.method == 'POST':
        # Implementation depends on your cart system
        return JsonResponse({'success': True, 'message': 'Cart updated'})
    return JsonResponse({'success': False, 'message': 'Invalid request'})


def add_to_favorites(request):
    """Add item to favorites via AJAX"""
    if request.method == 'POST':
        # Implementation depends on your favorites system
        return JsonResponse({'success': True, 'message': 'Product added to favorites'})
    return JsonResponse({'success': False, 'message': 'Invalid request'})


def remove_from_favorites(request):
    """Remove item from favorites via AJAX"""
    if request.method == 'POST':
        # Implementation depends on your favorites system
        return JsonResponse({'success': True, 'message': 'Product removed from favorites'})
    return JsonResponse({'success': False, 'message': 'Invalid request'})
