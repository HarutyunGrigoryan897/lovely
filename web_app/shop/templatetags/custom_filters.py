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


@register.filter
def user_price(product, user):
    """
    Get price for product with user level multiplier applied
    Usage: {{ product|user_price:request.user }}
    """
    if hasattr(product, 'get_display_price_for_user'):
        return product.get_display_price_for_user(user)
    return product.display_price


@register.simple_tag(takes_context=True)
def get_user_price(context, product):
    """
    Get price for product with current user's multiplier
    Usage: {% get_user_price product %}
    """
    user = context.get('request').user if context.get('request') else None
    if hasattr(product, 'get_display_price_for_user'):
        return product.get_display_price_for_user(user)
    return product.display_price


@register.filter
def multiply_price(price, user):
    """
    Multiply a price by user's level multiplier
    Usage: {{ price|multiply_price:request.user }}
    """
    from authorization.models import UserLevelMultiplier
    
    if not price:
        return Decimal('0.00')
    
    if user and user.is_authenticated and hasattr(user, 'get_price_multiplier'):
        multiplier = Decimal(str(user.get_price_multiplier()))
    else:
        # Use default multiplier from UserLevelMultiplier model
        multiplier = Decimal(str(UserLevelMultiplier.get_default_multiplier()))
    
    return Decimal(str(price)) * multiplier


@register.simple_tag(takes_context=True)
def get_gold_price_per_gram(context):
    """
    Get current gold price per gram with user multiplier
    Usage: {% get_gold_price_per_gram %}
    """
    from shop.models import GoldPrice
    from authorization.models import UserLevelMultiplier
    
    user = context.get('request').user if context.get('request') else None
    
    base_price = GoldPrice.get_current_price()
    
    if user and user.is_authenticated and hasattr(user, 'get_price_multiplier'):
        multiplier = Decimal(str(user.get_price_multiplier()))
    else:
        # Use default multiplier from UserLevelMultiplier model
        multiplier = Decimal(str(UserLevelMultiplier.get_default_multiplier()))
    
    return base_price * multiplier


@register.simple_tag(takes_context=True)
def get_work_price(context):
    """
    Get current work price with user multiplier
    Usage: {% get_work_price %}
    """
    from shop.models import WorkPrice
    from authorization.models import UserLevelMultiplier
    
    user = context.get('request').user if context.get('request') else None
    
    base_price = WorkPrice.get_current_price()
    
    if user and user.is_authenticated and hasattr(user, 'get_price_multiplier'):
        multiplier = Decimal(str(user.get_price_multiplier()))
    else:
        # Use default multiplier from UserLevelMultiplier model
        multiplier = Decimal(str(UserLevelMultiplier.get_default_multiplier()))
    
    return base_price * multiplier

