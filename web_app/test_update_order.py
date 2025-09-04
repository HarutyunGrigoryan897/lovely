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

# Get the first user with orders
user = CustomUser.objects.get(username='harutyungrigoryan00')
print(f'User: {user.username}')
print(f'Date joined: {user.date_joined}')

# Get orders for this user
orders = Order.objects.filter(user=user)
print(f'Total orders: {orders.count()}')

# Update one order to confirmed status to test total spent
if orders.exists():
    test_order = orders.first()
    print(f'Updating order {test_order.order_number} from {test_order.status} to confirmed')
    test_order.status = 'confirmed'
    test_order.save()
    
    # Recalculate total spent
    total_spent = Order.objects.filter(
        user=user, 
        status__in=['confirmed', 'processing', 'shipped', 'delivered']
    ).aggregate(total=models.Sum('total_amount'))['total'] or Decimal('0.00')
    
    print(f'New total spent: ${total_spent}')
else:
    print('No orders found for this user')
