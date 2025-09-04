#!/usr/bin/env python
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from django.db import models
from authorization.models import CustomUser
from shop.models import Order, Product, Brand, Category
from decimal import Decimal

# Check if we have any users
print('Current users in database:')
for user in CustomUser.objects.all()[:5]:
    print(f'- {user.username or user.telegram_id} (ID: {user.id})')

# Check if we have any orders
print('\nCurrent orders in database:')
for order in Order.objects.all()[:5]:
    print(f'- Order {order.order_number}: ${order.total_amount} ({order.status})')

print('\nUser statistics:')
for user in CustomUser.objects.all()[:3]:
    orders_count = Order.objects.filter(user=user).count()
    total_spent = Order.objects.filter(
        user=user, 
        status__in=['confirmed', 'processing', 'shipped', 'delivered']
    ).aggregate(total=models.Sum('total_amount'))['total'] or Decimal('0.00')
    print(f'User {user.username or user.telegram_id}: {orders_count} orders, ${total_spent} spent, joined {user.date_joined.strftime("%b %Y")}')
