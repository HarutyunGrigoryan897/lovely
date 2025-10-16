from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.db.models import Q, Sum, Count
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from decimal import Decimal
import json
import logging
from .models import Product, Category, Brand, WatchSpecification, JewelrySpecification, ProductCustomization, Cart, CartItem, Order, OrderItem, HeroSection, ShippingAddress
from .scraper import should_update_gold_price, update_gold_price_sync

logger = logging.getLogger(__name__)


def index(request):
    """Homepage with featured products"""
    # Check if gold price needs updating (every 1 minute) - runs silently in background
    if should_update_gold_price():
        logger.info("Gold price update needed. Starting scraping process...")
        success, message = update_gold_price_sync()
        if success:
            logger.info(f"Gold price update successful")
        else:
            logger.error(f"Gold price update failed")
    
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
    
    # Get authenticated user for price calculations
    user = request.user if request.user.is_authenticated else None
    
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
    
    # Pre-calculate initial pricing with user multiplier
    initial_pricing = None
    gold_rate = None
    work_rate = None
    
    if product.gold_weight_grams or product.has_diamonds:
        # Get default diamond quantities from diamond options
        diamond_quantities = {}
        for option in product.diamond_options.all():
            diamond_quantities[option.size_category] = 0  # Start with 0 for user to configure
        
        # Calculate initial pricing (without diamonds, just gold + work)
        initial_pricing = product.calculate_base_price(diamond_quantities, user=user)
        
        # Get rates for display (already includes user multiplier)
        if product.gold_weight_grams:
            from .models import GoldPrice
            base_gold_rate = GoldPrice.get_current_price()
            # Apply user multiplier to the rate
            if user and hasattr(user, 'get_price_multiplier'):
                multiplier = user.get_price_multiplier()
                gold_rate = float(base_gold_rate * multiplier)
            else:
                gold_rate = float(base_gold_rate * Decimal('1.8'))  # Default multiplier
        
        # Get work price with multiplier
        from .models import WorkPrice
        base_work_price = WorkPrice.get_current_price()
        if user and hasattr(user, 'get_price_multiplier'):
            multiplier = user.get_price_multiplier()
            work_rate = float(base_work_price * multiplier)
        else:
            work_rate = float(base_work_price * Decimal('1.8'))  # Default multiplier
    
    # Get user's price multiplier for frontend
    user_multiplier = 1.8  # Default
    if user and hasattr(user, 'get_price_multiplier'):
        user_multiplier = float(user.get_price_multiplier())
    
    context = {
        'product': product,
        'additional_images': additional_images,
        'watch_specs': watch_specs,
        'jewelry_specs': jewelry_specs,
        'customization_groups': customization_groups,
        'related_products': related_products,
        'initial_pricing': initial_pricing,
        'gold_rate': gold_rate,
        'work_rate': work_rate,
        'user_multiplier': user_multiplier,
        'user_price': product.get_display_price(user),  # Pre-calculated user-specific price
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
    print("\n" + "="*80)
    print("🔷 [DJANGO] add_to_cart_api called")
    print(f"🎯 [DJANGO] REQUEST SOURCE: {request.headers.get('X-Request-Source', 'UNKNOWN')}")
    print("="*80)
    
    try:
        data = json.loads(request.body)
        print(f"📥 [DJANGO] Received data: {data}")
        
        product_slug = data.get('product_id')
        quantity = int(data.get('quantity', 1))
        customization_data = data.get('customization', {})
        customization_price = Decimal(data.get('customization_price', '0.00'))
        unit_price = data.get('unit_price')  # Get custom unit price if provided
        
        print(f"📦 [DJANGO] Parsed: product_slug={product_slug}, quantity={quantity}, unit_price={unit_price}")
        
        # Validate inputs
        if not product_slug:
            return JsonResponse({'success': False, 'error': 'Product ID is required'}, status=400)
        
        if quantity < 1:
            return JsonResponse({'success': False, 'error': 'Quantity must be at least 1'}, status=400)
        
        # Get product
        try:
            product = Product.objects.get(slug=product_slug, is_active=True)
            print(f"✅ [DJANGO] Product found: {product.name} (ID: {product.id})")
        except Product.DoesNotExist:
            print(f"❌ [DJANGO] Product not found: {product_slug}")
            return JsonResponse({'success': False, 'error': 'Product not found'}, status=404)
        
        # Check stock
        if product.stock_status == 'out_of_stock':
            return JsonResponse({'success': False, 'error': 'Product is out of stock'}, status=400)
        
        # Use provided unit price (calculated from frontend) or product's display price
        if unit_price is None:
            unit_price = product.display_price
        else:
            unit_price = Decimal(str(unit_price))
        
        # Get or create cart
        cart = get_or_create_cart(request.user)
        print(f"🛒 [DJANGO] Cart ID: {cart.id}, Current items: {cart.total_items}")
        
        # Normalize empty customization data
        if not customization_data or customization_data == {}:
            customization_data = None
        
        print(f"🔍 [DJANGO] Checking for existing cart item...")
        # Check if item with same customization already exists
        existing_item = None
        if customization_data:
            # For items with customization, match exactly
            existing_item = CartItem.objects.filter(
                cart=cart,
                product=product,
                customization_data=customization_data
            ).first()
        else:
            # For items without customization, find any without customization
            existing_item = CartItem.objects.filter(
                cart=cart,
                product=product,
                customization_data__isnull=True
            ).first()
            
            # Also check for empty dict
            if not existing_item:
                existing_item = CartItem.objects.filter(
                    cart=cart,
                    product=product,
                    customization_data={}
                ).first()
        
        if existing_item:
            # Update quantity
            print(f"♻️ [DJANGO] Existing item found! Current qty: {existing_item.quantity}, adding: {quantity}")
            existing_item.quantity += quantity
            existing_item.save()
            cart_item = existing_item
            print(f"♻️ [DJANGO] Updated item quantity to: {existing_item.quantity}")
        else:
            # Create new cart item
            print(f"➕ [DJANGO] Creating new cart item with quantity: {quantity}")
            cart_item = CartItem.objects.create(
                cart=cart,
                product=product,
                quantity=quantity,
                customization_data=customization_data,
                customization_price=customization_price,
                unit_price=unit_price
            )
            print(f"➕ [DJANGO] New cart item created with ID: {cart_item.id}")
        
        print(f"🛒 [DJANGO] Cart now has {cart.total_items} items, total: ${cart.total_price}")
        print("="*80 + "\n")
        
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
                    'image_url': item.product.image.url if item.product.image else None,
                    'price': float(item.unit_price),
                },
                'quantity': item.quantity,
                'price': float(item.total_price),
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
            },
            'cart_item_count': cart.total_items,  # Total quantity for badge
            'cart_total': float(cart.total_price)
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
        
        # Get shipping address ID from request
        data = json.loads(request.body)
        shipping_address_id = data.get('shipping_address_id')
        
        if not shipping_address_id:
            return JsonResponse({'success': False, 'error': 'Please select a shipping address'}, status=400)
        
        # Get the shipping address
        try:
            shipping_address = ShippingAddress.objects.get(id=shipping_address_id, user=user)
        except ShippingAddress.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Invalid shipping address'}, status=400)
        
        # Create the order with shipping information
        order = Order.objects.create(
            user=user,
            total_amount=total_amount,
            total_items=total_items,
            customer_email=data.get('customer_email', user.email),
            customer_first_name=user.first_name or '',
            customer_last_name=user.last_name or '',
            # Reference to the shipping address
            shipping_address_ref=shipping_address,
            # Snapshot of shipping information
            shipping_first_name=shipping_address.first_name or '',
            shipping_last_name=shipping_address.last_name or '',
            shipping_address=shipping_address.address,
            shipping_city=shipping_address.city,
            shipping_zip_code=shipping_address.zip_code,
            shipping_country=shipping_address.country,
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
        
    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'error': 'Invalid request data'}, status=400)
    except Exception as e:
        return JsonResponse({'success': False, 'error': f'Failed to create order: {str(e)}'}, status=500)


# ============== SHIPPING ADDRESS VIEWS ==============

@login_required
def get_shipping_addresses(request):
    """Get all shipping addresses for the current user"""
    try:
        # Check if user is authenticated
        if not request.user.is_authenticated:
            return JsonResponse({'success': False, 'error': 'Authentication required'}, status=401)
        
        addresses = ShippingAddress.objects.filter(user=request.user)
        addresses_data = [{
            'id': addr.id,
            'label': addr.label,
            'first_name': addr.first_name,
            'last_name': addr.last_name,
            'address': addr.address,
            'city': addr.city,
            'zip_code': addr.zip_code,
            'country': addr.country,
            'is_default': addr.is_default,
        } for addr in addresses]
        
        return JsonResponse({
            'success': True,
            'addresses': addresses_data
        })
    except Exception as e:
        return JsonResponse({'success': False, 'error': f'Failed to fetch addresses: {str(e)}'}, status=500)


@csrf_exempt
@require_POST
def add_shipping_address(request):
    """Add a new shipping address"""
    try:
        # Check if user is authenticated
        if not request.user.is_authenticated:
            return JsonResponse({'success': False, 'error': 'Authentication required'}, status=401)
        
        data = json.loads(request.body)
        
        # Validate required fields
        required_fields = ['label', 'first_name', 'last_name', 'address', 'city', 'zip_code', 'country']
        for field in required_fields:
            if not data.get(field):
                return JsonResponse({'success': False, 'error': f'{field.replace("_", " ").title()} is required'}, status=400)
        
        # Create the address
        address = ShippingAddress.objects.create(
            user=request.user,
            label=data['label'],
            first_name=data['first_name'],
            last_name=data['last_name'],
            address=data['address'],
            city=data['city'],
            zip_code=data['zip_code'],
            country=data['country'],
            is_default=data.get('is_default', False)
        )
        
        return JsonResponse({
            'success': True,
            'message': 'Address added successfully',
            'address': {
                'id': address.id,
                'label': address.label,
                'first_name': address.first_name,
                'last_name': address.last_name,
                'address': address.address,
                'city': address.city,
                'zip_code': address.zip_code,
                'country': address.country,
                'is_default': address.is_default,
            }
        })
    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'error': 'Invalid JSON data'}, status=400)
    except Exception as e:
        return JsonResponse({'success': False, 'error': f'Failed to add address: {str(e)}'}, status=500)


@csrf_exempt
@require_POST
def update_shipping_address(request, address_id):
    """Update an existing shipping address"""
    try:
        # Check if user is authenticated
        if not request.user.is_authenticated:
            return JsonResponse({'success': False, 'error': 'Authentication required'}, status=401)
        
        data = json.loads(request.body)
        
        # Get the address
        try:
            address = ShippingAddress.objects.get(id=address_id, user=request.user)
        except ShippingAddress.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Address not found'}, status=404)
        
        # Update fields
        address.label = data.get('label', address.label)
        address.first_name = data.get('first_name', address.first_name)
        address.last_name = data.get('last_name', address.last_name)
        address.address = data.get('address', address.address)
        address.city = data.get('city', address.city)
        address.zip_code = data.get('zip_code', address.zip_code)
        address.country = data.get('country', address.country)
        address.is_default = data.get('is_default', address.is_default)
        address.save()
        
        return JsonResponse({
            'success': True,
            'message': 'Address updated successfully',
            'address': {
                'id': address.id,
                'label': address.label,
                'first_name': address.first_name,
                'last_name': address.last_name,
                'address': address.address,
                'city': address.city,
                'zip_code': address.zip_code,
                'country': address.country,
                'is_default': address.is_default,
            }
        })
    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'error': 'Invalid JSON data'}, status=400)
    except Exception as e:
        return JsonResponse({'success': False, 'error': f'Failed to update address: {str(e)}'}, status=500)


@csrf_exempt
@require_POST
def delete_shipping_address(request, address_id):
    """Delete a shipping address"""
    try:
        # Check if user is authenticated
        if not request.user.is_authenticated:
            return JsonResponse({'success': False, 'error': 'Authentication required'}, status=401)
        
        # Get the address
        try:
            address = ShippingAddress.objects.get(id=address_id, user=request.user)
        except ShippingAddress.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Address not found'}, status=404)
        
        address.delete()
        
        return JsonResponse({
            'success': True,
            'message': 'Address deleted successfully'
        })
    except Exception as e:
        return JsonResponse({'success': False, 'error': f'Failed to delete address: {str(e)}'}, status=500)


@csrf_exempt
@require_POST
def set_default_address(request, address_id):
    """Set an address as default"""
    try:
        # Check if user is authenticated
        if not request.user.is_authenticated:
            return JsonResponse({'success': False, 'error': 'Authentication required'}, status=401)
        
        # Get the address
        try:
            address = ShippingAddress.objects.get(id=address_id, user=request.user)
        except ShippingAddress.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Address not found'}, status=404)
        
        # Set as default (the model's save method will handle removing default from others)
        address.is_default = True
        address.save()
        
        return JsonResponse({
            'success': True,
            'message': 'Default address updated'
        })
    except Exception as e:
        return JsonResponse({'success': False, 'error': f'Failed to set default address: {str(e)}'}, status=500)


@csrf_exempt
@require_POST
def calculate_product_price(request, product_slug):
    """Calculate product price based on diamond quantities and type"""
    try:
        product = get_object_or_404(Product, slug=product_slug, is_active=True)
        
        # Parse diamond quantities and type from request
        data = json.loads(request.body)
        diamond_quantities = data.get('diamond_quantities', {})
        diamond_type = data.get('diamond_type', product.diamond_type or 'natural')
        
        # Temporarily override product's diamond type for calculation
        original_type = product.diamond_type
        product.diamond_type = diamond_type
        
        # Calculate price breakdown with user multiplier
        user = request.user if request.user.is_authenticated else None
        pricing = product.calculate_base_price(diamond_quantities, user=user)
        
        # Restore original type
        product.diamond_type = original_type
        
        return JsonResponse({
            'success': True,
            'pricing': {
                'gold_price': float(pricing['gold_price']),
                'diamond_price': float(pricing['diamond_price']),
                'work_price': float(pricing['work_price']),
                'total_price': float(pricing['total_price']),
            },
            'product': {
                'name': product.name,
                'brand': product.brand.name,
                'gold_weight_grams': float(product.gold_weight_grams),
                'has_diamonds': product.has_diamonds,
                'diamond_type': diamond_type,
            },
        })
    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'error': 'Invalid JSON data'}, status=400)
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)


def get_product_details(request, product_slug):
    """Get detailed product information including pricing options"""
    try:
        product = get_object_or_404(Product, slug=product_slug, is_active=True)
        
        # Get default diamond quantities
        diamond_quantities = {}
        diamond_options = []
        
        for option in product.diamond_options.all():
            diamond_quantities[option.size_category] = option.default_quantity
            diamond_options.append({
                'size_category': option.size_category,
                'size_label': option.get_size_category_display(),
                'default_quantity': option.default_quantity,
                'min_quantity': option.min_quantity,
                'max_quantity': option.max_quantity,
            })
        
        # Calculate default price with user multiplier
        user = request.user if request.user.is_authenticated else None
        pricing = product.calculate_base_price(diamond_quantities, user=user) if product.has_diamonds else None
        
        return JsonResponse({
            'success': True,
            'product': {
                'id': product.id,
                'name': product.name,
                'slug': product.slug,
                'brand': product.brand.name,
                'description': product.description,
                'gold_weight_grams': float(product.gold_weight_grams) if product.gold_weight_grams else 0,
                'has_diamonds': product.has_diamonds,
                'diamond_type': product.diamond_type,
                'diamond_type_display': product.get_diamond_type_display() if product.diamond_type else None,
            },
            'diamond_options': diamond_options,
            'pricing': {
                'gold_price': float(pricing['gold_price']) if pricing else 0,
                'diamond_price': float(pricing['diamond_price']) if pricing else 0,
                'work_price': float(pricing['work_price']) if pricing else 0,
                'total_price': float(pricing['total_price']) if pricing else 0,
            } if pricing else None,
        })
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)


def get_diamond_prices(request):
    """Get all diamond prices for both natural and lab diamonds"""
    from .models import DiamondPrice
    try:
        prices = {
            'natural': {},
            'lab': {}
        }
        
        for dp in DiamondPrice.objects.filter(is_active=True):
            prices[dp.diamond_type][dp.size_category] = float(dp.price_per_unit)
        
        return JsonResponse({
            'success': True,
            'prices': prices
        })
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)


# -------------------- ORDER MANAGEMENT API (for Telegram Bot) --------------------
from authorization.bot_authentication import BotAuthentication
from rest_framework.decorators import api_view, authentication_classes
from rest_framework.response import Response
from rest_framework import status as http_status

@api_view(['POST'])
@authentication_classes([BotAuthentication])
def update_order_status(request, order_id):
    """Update order status (for admin/bot use)"""
    try:
        order = Order.objects.get(id=order_id)
        new_status = request.data.get('status')
        
        if new_status not in dict(Order.ORDER_STATUS_CHOICES):
            return Response({
                'success': False,
                'error': 'Invalid status'
            }, status=http_status.HTTP_400_BAD_REQUEST)
        
        order.status = new_status
        order.save()
        
        return Response({
            'success': True,
            'order_id': order.id,
            'order_number': order.order_number,
            'status': order.status,
            'status_display': order.get_status_display()
        })
    except Order.DoesNotExist:
        return Response({
            'success': False,
            'error': 'Order not found'
        }, status=http_status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({
            'success': False,
            'error': str(e)
        }, status=http_status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@authentication_classes([BotAuthentication])
def get_order_details(request, order_id):
    """Get detailed order information (for admin/bot use)"""
    try:
        order = Order.objects.select_related('user', 'shipping_address_ref').prefetch_related(
            'items__product__brand',
            'items__product__category',
            'items__product__watch_specs'
        ).get(id=order_id)
        
        # Build order items data
        items_data = []
        for item in order.items.all():
            product = item.product
            item_info = {
                'id': item.id,
                'product_name': product.name,
                'brand': product.brand.name,
                'quantity': item.quantity,
                'price': float(item.price),
                'total': float(item.total_price),
                'sku': product.sku,
                'model_number': product.model_number,
                'customization_data': item.customization_data,
            }
            
            # Add watch specs if available
            if hasattr(product, 'watch_specs') and product.watch_specs:
                watch = product.watch_specs
                item_info['watch_specs'] = {
                    'case_material': watch.get_case_material_display() if watch.case_material else None,
                    'case_size': watch.case_size,
                    'movement': watch.get_movement_display() if watch.movement else None,
                    'dial_color': watch.dial_color,
                    'water_resistance': watch.water_resistance,
                }
            
            items_data.append(item_info)
        
        order_data = {
            'id': order.id,
            'order_number': order.order_number,
            'status': order.status,
            'status_display': order.get_status_display(),
            'total_amount': float(order.total_amount),
            'total_items': order.total_items,
            'customer_email': order.customer_email,
            'customer_first_name': order.customer_first_name,
            'customer_last_name': order.customer_last_name,
            'shipping_address': {
                'first_name': order.shipping_first_name,
                'last_name': order.shipping_last_name,
                'address': order.shipping_address,
                'city': order.shipping_city,
                'zip_code': order.shipping_zip_code,
                'country': order.shipping_country,
            },
            'items': items_data,
            'created_at': order.created_at.isoformat(),
            'user': {
                'id': order.user.id,
                'username': order.user.username,
                'telegram_id': order.user.telegram_id,
            }
        }
        
        return Response({
            'success': True,
            'order': order_data
        })
    except Order.DoesNotExist:
        return Response({
            'success': False,
            'error': 'Order not found'
        }, status=http_status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({
            'success': False,
            'error': str(e)
        }, status=http_status.HTTP_500_INTERNAL_SERVER_ERROR)
