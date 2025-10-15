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
