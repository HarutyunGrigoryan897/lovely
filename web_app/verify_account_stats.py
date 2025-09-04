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

print("Account Statistics for All Users:")
print("=" * 50)

for user in CustomUser.objects.all():
    # Calculate orders count
    orders_count = Order.objects.filter(user=user).count()
    
    # Calculate total spent (sum of all completed orders)
    total_spent_aggregate = Order.objects.filter(
        user=user,
        status__in=['confirmed', 'processing', 'shipped', 'delivered']
    ).aggregate(total=models.Sum('total_amount'))
    
    total_spent = total_spent_aggregate['total'] or Decimal('0.00')
    
    # Show pending orders value for reference
    pending_orders_aggregate = Order.objects.filter(
        user=user,
        status='pending'
    ).aggregate(total=models.Sum('total_amount'))
    
    pending_total = pending_orders_aggregate['total'] or Decimal('0.00')
    
    print(f"User: {user.username or user.telegram_id}")
    print(f"  Total Orders: {orders_count}")
    print(f"  Total Spent (confirmed orders): ${total_spent}")
    print(f"  Pending Orders Value: ${pending_total}")
    print(f"  Member Since: {user.date_joined.strftime('%b %Y')}")
    print()
