"""
Context processors for shop app
"""
from decimal import Decimal


def user_pricing(request):
    """
    Add user pricing multiplier to template context
    """
    from authorization.models import UserLevelMultiplier
    
    if request.user.is_authenticated and hasattr(request.user, 'get_price_multiplier'):
        multiplier = request.user.get_price_multiplier()
    else:
        # Use default multiplier from UserLevelMultiplier model
        multiplier = UserLevelMultiplier.get_default_multiplier()
    
    return {
        'user_price_multiplier': multiplier,
        'user': request.user
    }
