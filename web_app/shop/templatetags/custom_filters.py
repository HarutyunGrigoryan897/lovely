from django import template
from decimal import Decimal

register = template.Library()

@register.filter
def replace(value, arg):
    """
    Replace all occurrences of the old string with the new string.
    Usage: {{ value|replace:"old,new" }}
    """
    if not value:
        return value
    
    try:
        old, new = arg.split(',')
        return value.replace(old, new)
    except ValueError:
        return value


@register.simple_tag(takes_context=True)
def user_price(context, product, size_label=None, diamond_type=None):
    """
    Get product price with user level multiplier applied
    Supports size and diamond type parameters
    Usage: {% user_price product %} or {% user_price product size_label="19mm" diamond_type="natural" %}
    """
    request = context.get('request')
    user = request.user if request and request.user.is_authenticated else None
    
    # Get size multiplier if size_label provided
    size_multiplier = Decimal('1.0')
    if size_label:
        try:
            from shop.models import ProductSize
            product_size = ProductSize.objects.get(product=product, size_label=size_label)
            size_multiplier = product_size.price_multiplier
        except:
            pass
    
    return product.get_display_price(
        user=user,
        size_multiplier=size_multiplier,
        diamond_type=diamond_type
    )


@register.filter
def user_price_filter(product, request):
    """
    Filter version: Get product price with user level multiplier applied (basic version without size/diamond)
    Usage: {{ product|user_price_filter:request }}
    """
    if request and request.user.is_authenticated:
        return product.get_display_price(request.user, size_multiplier=None, diamond_type=None)
    return product.get_display_price()


@register.simple_tag(takes_context=True)
def calculate_product_price(context, product, size_label=None, diamond_type=None):
    """
    Calculate complete product price breakdown
    Returns the total price with all multipliers applied
    Usage: {% calculate_product_price product size_label="19mm" diamond_type="natural" %}
    """
    request = context.get('request')
    user = request.user if request and request.user.is_authenticated else None
    
    # Get size multiplier if size_label provided
    size_multiplier = Decimal('1.0')
    if size_label:
        try:
            from shop.models import ProductSize
            product_size = ProductSize.objects.get(product=product, size_label=size_label)
            size_multiplier = product_size.price_multiplier
        except:
            pass
    
    price_breakdown = product.calculate_base_price(
        diamond_type=diamond_type,
        user=user,
        size_multiplier=size_multiplier
    )
    
    return price_breakdown['total_price']

