#!/usr/bin/env python
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from django.db import models
from authorization.models import CustomUser
from shop.models import Order
from decimal import Decimal

def get_user_stats(user):
    """Get account statistics for a user (same logic as in views.py)"""
    orders_count = Order.objects.filter(user=user).count()
    
    # Calculate total spent (confirmed orders only)
    total_spent_aggregate = Order.objects.filter(
        user=user,
        status__in=['confirmed', 'processing', 'shipped', 'delivered']
    ).aggregate(total=models.Sum('total_amount'))
    
    total_spent = total_spent_aggregate['total'] or Decimal('0.00')
    
    # Calculate total order value (all orders)
    total_value_aggregate = Order.objects.filter(
        user=user
    ).aggregate(total=models.Sum('total_amount'))
    
    total_order_value = total_value_aggregate['total'] or Decimal('0.00')
    
    return orders_count, total_spent, total_order_value

print("Enhanced Account Statistics:")
print("=" * 60)

for user in CustomUser.objects.all():
    orders_count, total_spent, total_order_value = get_user_stats(user)
    
    print(f"User: {user.username or user.telegram_id}")
    print(f"  📊 Total Orders: {orders_count}")
    print(f"  💰 Total Spent (confirmed): ${total_spent:,.2f}")
    print(f"  📋 Total Order Value (all): ${total_order_value:,.2f}")
    
    if total_order_value > total_spent:
        pending_value = total_order_value - total_spent
        print(f"  ⏳ Pending Orders Value: ${pending_value:,.2f}")
    
    print(f"  📅 Member Since: {user.date_joined.strftime('%b %Y')}")
    print("-" * 40)

# Also show order breakdown by status
print("\nOrder Status Breakdown:")
print("=" * 30)
statuses = ['pending', 'confirmed', 'processing', 'shipped', 'delivered', 'cancelled']
for status in statuses:
    count = Order.objects.filter(status=status).count()
    total = Order.objects.filter(status=status).aggregate(
        total=models.Sum('total_amount'))['total'] or Decimal('0.00')
    if count > 0:
        print(f"{status.capitalize()}: {count} orders, ${total:,.2f}")
