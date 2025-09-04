from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.db.models import Q, Sum, Count
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from decimal import Decimal
import json
from .models import Product, Category, Brand, WatchSpecification, JewelrySpecification, ProductCustomization, Cart, CartItem, Order, OrderItem, HeroSection


def index(request):
    """Homepage with featured products"""
    featured_products = Product.objects.filter(
        is_active=True, 
        show_on_homepage=True
    ).select_related('brand', 'category')[:8]
    categories = Category.objects.filter(is_active=True, parent=None).order_by('sort_order')
    brands = Brand.objects.filter(is_active=True, show_on_homepage=True)[:6]
    hero_section = HeroSection.get_active_hero()
    
    context = {
        'featured_products': featured_products,
        'categories': categories,
        'brands': brands,
        'hero_section': hero_section,
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
    
    # Get all products for JavaScript filtering (without pagination)
    all_products = Product.objects.filter(is_active=True).select_related('brand', 'category').order_by('name')
    
    context = {
        'page_obj': page_obj,
        'products': page_obj.object_list,
        'all_products': all_products,  # For JavaScript filtering
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
    
    # Get additional product images
    additional_images = product.additional_images.all().order_by('sort_order')
    
    # Get related products
    related_products = Product.objects.filter(
        category=product.category,
        is_active=True
    ).exclude(id=product.id).select_related('brand', 'category')[:4]
    
    context = {
        'product': product,
        'additional_images': additional_images,
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


def favorites(request):
    """Favorites/Wishlist page"""
    context = {}
    return render(request, 'favorites.html', context)


def account(request):
    """User account page"""
    recent_orders = []
    orders_count = 0
    total_spent = Decimal('0.00')
    total_order_value = Decimal('0.00')
    member_since = None
    
    if request.user.is_authenticated:
        # Get recent orders
        recent_orders = Order.objects.filter(user=request.user).order_by('-created_at')[:5]
        
        # Calculate orders count
        orders_count = Order.objects.filter(user=request.user).count()
        
        # Calculate total spent (sum of confirmed/processed/shipped/delivered orders only)
        total_spent_aggregate = Order.objects.filter(
            user=request.user,
            status__in=['confirmed', 'processing', 'shipped', 'delivered']
        ).aggregate(total=Sum('total_amount'))
        
        total_spent = total_spent_aggregate['total'] or Decimal('0.00')
        
        # Calculate total order value (all orders regardless of status)
        total_value_aggregate = Order.objects.filter(
            user=request.user
        ).aggregate(total=Sum('total_amount'))
        
        total_order_value = total_value_aggregate['total'] or Decimal('0.00')
        
        # Get member since date (user registration date)
        member_since = request.user.date_joined
    
    context = {
        'user': request.user if request.user.is_authenticated else None,
        'is_telegram_user': bool(getattr(request.user, 'telegram_id', None)) if request.user.is_authenticated else False,
        'recent_orders': recent_orders,
        'orders_count': orders_count,
        'total_spent': total_spent,
        'total_order_value': total_order_value,
        'member_since': member_since,
    }
    return render(request, 'account.html', context)


def settings(request):
    """User settings page"""
    context = {}
    return render(request, 'settings.html', context)


@login_required
def orders(request):
    """User orders page"""
    user_orders = Order.objects.filter(user=request.user).prefetch_related('items__product')
    context = {
        'orders': user_orders
    }
    return render(request, 'orders.html', context)


def order_confirmation(request, order_id=None):
    """Order confirmation page"""
    context = {}
    
    if order_id:
        try:
            # Get the order if user is authenticated and owns the order
            if request.user.is_authenticated:
                order = Order.objects.get(id=order_id, user=request.user)
                context['order'] = order
                context['order_items'] = order.items.all()
            else:
                # Redirect to login if not authenticated
                return redirect('/')
        except Order.DoesNotExist:
            # Order not found or doesn't belong to user
            context['error'] = 'Order not found'
    
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


def add_to_cart(request):
    """Add item to cart via AJAX"""
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


# ============== CART VIEWS ==============

def get_or_create_cart(user):
    """Helper function to get or create cart for user"""
    cart, created = Cart.objects.get_or_create(user=user)
    return cart


@csrf_exempt
@require_POST
@login_required
def add_to_cart_api(request):
    """Add item to cart via AJAX API"""
    try:
        data = json.loads(request.body)
        product_slug = data.get('product_id')
        quantity = int(data.get('quantity', 1))
        customization_data = data.get('customization', {})
        customization_price = Decimal(data.get('customization_price', '0.00'))
        
        # Validate inputs
        if not product_slug:
            return JsonResponse({'success': False, 'error': 'Product ID is required'}, status=400)
        
        if quantity < 1:
            return JsonResponse({'success': False, 'error': 'Quantity must be at least 1'}, status=400)
        
        # Get product
        try:
            product = Product.objects.get(slug=product_slug, is_active=True)
        except Product.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Product not found'}, status=404)
        
        # Check stock
        if product.stock_status == 'out_of_stock':
            return JsonResponse({'success': False, 'error': 'Product is out of stock'}, status=400)
        
        # Get or create cart
        cart = get_or_create_cart(request.user)
        
        # Check if item with same customization already exists
        existing_item = CartItem.objects.filter(
            cart=cart,
            product=product,
            customization_data=customization_data
        ).first()
        
        if existing_item:
            # Update quantity
            existing_item.quantity += quantity
            existing_item.save()
            cart_item = existing_item
        else:
            # Create new cart item
            cart_item = CartItem.objects.create(
                cart=cart,
                product=product,
                quantity=quantity,
                customization_data=customization_data,
                customization_price=customization_price,
                unit_price=product.price
            )
        
        return JsonResponse({
            'success': True,
            'message': f'Added {quantity} item(s) to cart',
            'cart_item_count': cart.total_items,
            'cart_total': float(cart.total_price)
        })
        
    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'error': 'Invalid JSON data'}, status=400)
    except ValueError as e:
        return JsonResponse({'success': False, 'error': f'Invalid data: {str(e)}'}, status=400)
    except Exception as e:
        return JsonResponse({'success': False, 'error': f'Server error: {str(e)}'}, status=500)


@csrf_exempt
@require_POST
@login_required
def update_cart_item(request):
    """Update cart item quantity"""
    try:
        data = json.loads(request.body)
        item_id = data.get('item_id')
        quantity = int(data.get('quantity', 1))
        
        if not item_id:
            return JsonResponse({'success': False, 'error': 'Item ID is required'}, status=400)
        
        if quantity < 1:
            return JsonResponse({'success': False, 'error': 'Quantity must be at least 1'}, status=400)
        
        # Get cart item
        cart = get_or_create_cart(request.user)
        try:
            cart_item = CartItem.objects.get(id=item_id, cart=cart)
        except CartItem.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Cart item not found'}, status=404)
        
        # Update quantity
        cart_item.quantity = quantity
        cart_item.save()
        
        return JsonResponse({
            'success': True,
            'message': 'Cart updated',
            'item_total': float(cart_item.total_price),
            'cart_total': float(cart.total_price),
            'cart_item_count': cart.total_items
        })
        
    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'error': 'Invalid JSON data'}, status=400)
    except ValueError as e:
        return JsonResponse({'success': False, 'error': f'Invalid data: {str(e)}'}, status=400)
    except Exception as e:
        return JsonResponse({'success': False, 'error': f'Server error: {str(e)}'}, status=500)


@csrf_exempt
@require_POST
@login_required
def remove_from_cart(request):
    """Remove item from cart"""
    try:
        data = json.loads(request.body)
        item_id = data.get('item_id')
        
        if not item_id:
            return JsonResponse({'success': False, 'error': 'Item ID is required'}, status=400)
        
        # Get cart item
        cart = get_or_create_cart(request.user)
        try:
            cart_item = CartItem.objects.get(id=item_id, cart=cart)
        except CartItem.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Cart item not found'}, status=404)
        
        # Remove item
        cart_item.delete()
        
        return JsonResponse({
            'success': True,
            'message': 'Item removed from cart',
            'cart_total': float(cart.total_price),
            'cart_item_count': cart.total_items
        })
        
    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'error': 'Invalid JSON data'}, status=400)
    except Exception as e:
        return JsonResponse({'success': False, 'error': f'Server error: {str(e)}'}, status=500)


@login_required
def get_cart_data(request):
    """Get cart data for user"""
    try:
        cart = get_or_create_cart(request.user)
        cart_items = []
        
        for item in cart.items.select_related('product', 'product__brand').all():
            cart_items.append({
                'id': item.id,
                'product': {
                    'slug': item.product.slug,
                    'name': item.customized_product_name,
                    'brand': item.product.brand.name,
                    'image': item.product.image.url if item.product.image else None,
                    'price': float(item.unit_price),
                },
                'quantity': item.quantity,
                'customization_price': float(item.customization_price),
                'total_price': float(item.total_price),
                'customization_data': item.customization_data
            })
        
        return JsonResponse({
            'success': True,
            'cart': {
                'items': cart_items,
                'total_items': cart.total_items,
                'total_price': float(cart.total_price),
                'item_count': cart.item_count
            }
        })
        
    except Exception as e:
        return JsonResponse({'success': False, 'error': f'Server error: {str(e)}'}, status=500)


@csrf_exempt
@require_POST
@login_required
def clear_cart(request):
    """Clear all items from cart"""
    try:
        cart = get_or_create_cart(request.user)
        cart.clear()
        
        return JsonResponse({
            'success': True,
            'message': 'Cart cleared',
            'cart_total': 0.0,
            'cart_item_count': 0
        })
        
    except Exception as e:
        return JsonResponse({'success': False, 'error': f'Server error: {str(e)}'}, status=500)


def remove_from_favorites(request):
    """Remove item from favorites via AJAX"""
    if request.method == 'POST':
        # Implementation depends on your favorites system
        return JsonResponse({'success': True, 'message': 'Product removed from favorites'})
    return JsonResponse({'success': False, 'message': 'Invalid request'})



@require_POST
@login_required
def create_order_from_cart(request):
    """Create an order from current cart items"""
    try:
        # Get user's cart
        cart, created = Cart.objects.get_or_create(user=request.user)
        cart_items = cart.items.all()
        
        if not cart_items.exists():
            return JsonResponse({'success': False, 'error': 'Cart is empty'}, status=400)
        
        # Create the order
        order = Order.objects.create(
            user=request.user,
            total_amount=cart.total_price,
            total_items=cart.total_items,
            customer_email=request.user.email,
            customer_first_name=getattr(request.user, 'first_name', ''),
            customer_last_name=getattr(request.user, 'last_name', ''),
        )
        
        # Create order items from cart items
        for cart_item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=cart_item.product,
                quantity=cart_item.quantity,
                price=cart_item.unit_price,
                customization_data=cart_item.customization_data
            )
        
        # Send telegram notification
        try:
            from .bot_utils import send_order_message
            send_order_message(order)
        except ImportError:
            pass  # bot_utils not available
        except Exception as e:
            print(f"Failed to send telegram notification: {e}")
        
        # Clear the cart after creating the order
        cart_items.delete()
        
        return JsonResponse({
            'success': True,
            'message': 'Order placed successfully',
            'order_number': order.order_number,
            'order_id': order.id
        })
        
    except Exception as e:
        return JsonResponse({'success': False, 'error': f'Failed to create order: {str(e)}'}, status=500)


def checkout(request):
    """Checkout page"""
    return render(request, 'checkout.html')


@csrf_exempt
@require_POST  
def process_checkout(request):
    """Process checkout form and create order"""
    try:
        # Get the user (for now, we'll create a guest user if not authenticated)
        if request.user.is_authenticated:
            user = request.user
        else:
            # For now, create a simple guest flow
            from django.contrib.auth import get_user_model
            User = get_user_model()
            user = User.objects.get(username='guest')  # You'll need to create this user
        
        # Get cart and cart items
        cart = get_or_create_cart(user)
        cart_items = cart.items.all()
        
        if not cart_items.exists():
            return JsonResponse({'success': False, 'error': 'Cart is empty'}, status=400)
        
        # Calculate totals
        total_amount = sum(item.unit_price * item.quantity for item in cart_items)
        total_items = sum(item.quantity for item in cart_items)
        
        # Create the order with shipping information
        order = Order.objects.create(
            user=user,
            total_amount=total_amount,
            total_items=total_items,
            customer_email=request.POST.get('customer_email', user.email),
            customer_first_name=user.first_name,
            customer_last_name=user.last_name,
            # Shipping information from form
            shipping_first_name=request.POST.get('shipping_first_name', ''),
            shipping_last_name=request.POST.get('shipping_last_name', ''),
            shipping_address=request.POST.get('shipping_address', ''),
            shipping_city=request.POST.get('shipping_city', ''),
            shipping_zip_code=request.POST.get('shipping_zip_code', ''),
            shipping_country=request.POST.get('shipping_country', ''),
        )
        
        # Create order items
        for cart_item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=cart_item.product,
                quantity=cart_item.quantity,
                price=cart_item.unit_price,
                customization_data=cart_item.customization_data
            )
        
        # Send telegram notification if bot_utils is available
        try:
            from .bot_utils import send_order_message
            send_order_message(order)
        except ImportError:
            pass  # bot_utils not available
        except Exception as e:
            print(f"Failed to send telegram notification: {e}")
        
        # Clear the cart after creating the order
        cart.clear()
        
        return JsonResponse({
            'success': True,
            'message': 'Order placed successfully',
            'order_number': order.order_number,
            'order_id': order.id
        })
        
    except Exception as e:
        return JsonResponse({'success': False, 'error': f'Failed to create order: {str(e)}'}, status=500)
