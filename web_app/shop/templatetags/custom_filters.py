from django import template

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
def user_price(context, product):
    """
    Get product price with user level multiplier applied
    Usage: {% user_price product %}
    """
    request = context.get('request')
    if request and request.user.is_authenticated:
        return product.get_display_price(request.user)
    return product.display_price


@register.filter
def user_price_filter(product, request):
    """
    Filter version: Get product price with user level multiplier applied
    Usage: {{ product|user_price_filter:request }}
    """
    if request and request.user.is_authenticated:
        return product.get_display_price(request.user)
    return product.display_price
