#!/usr/bin/env python
"""
Script to add sample products for testing pagination
Run this from the web_app directory with: python add_sample_products.py
"""

import os
import sys
import django
from decimal import Decimal
from django.utils.text import slugify

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from shop.models import Brand, Category, Product

def create_sample_data():
    """Create sample brands, categories, and products"""
    
    # Create brands if they don't exist
    brands_data = [
        {'name': 'Rolex', 'description': 'Swiss luxury watch manufacturer', 'country': 'Switzerland', 'founded_year': 1905},
        {'name': 'Patek Philippe', 'description': 'Swiss luxury watch and clock manufacturer', 'country': 'Switzerland', 'founded_year': 1839},
        {'name': 'Omega', 'description': 'Swiss luxury watchmaker', 'country': 'Switzerland', 'founded_year': 1848},
        {'name': 'Cartier', 'description': 'French luxury goods conglomerate', 'country': 'France', 'founded_year': 1847},
        {'name': 'Tiffany & Co.', 'description': 'American luxury jewelry and specialty retailer', 'country': 'USA', 'founded_year': 1837},
        {'name': 'Bulgari', 'description': 'Italian luxury brand', 'country': 'Italy', 'founded_year': 1884},
    ]
    
    brands = {}
    for brand_data in brands_data:
        brand, created = Brand.objects.get_or_create(
            name=brand_data['name'],
            defaults={
                'description': brand_data['description'],
                'country': brand_data['country'],
                'founded_year': brand_data['founded_year'],
                'is_active': True,
                'show_on_homepage': True
            }
        )
        brands[brand.name] = brand
        if created:
            print(f"Created brand: {brand.name}")
    
    # Create categories if they don't exist
    categories_data = [
        {'name': 'Luxury Watches', 'description': 'Premium timepieces'},
        {'name': 'Fine Jewelry', 'description': 'Exquisite jewelry pieces'},
        {'name': 'Men\'s Watches', 'description': 'Watches for men'},
        {'name': 'Women\'s Watches', 'description': 'Watches for women'},
        {'name': 'Rings', 'description': 'Beautiful rings'},
        {'name': 'Necklaces', 'description': 'Elegant necklaces'},
    ]
    
    categories = {}
    for cat_data in categories_data:
        category, created = Category.objects.get_or_create(
            name=cat_data['name'],
            defaults={
                'description': cat_data['description'],
                'is_active': True,
                'sort_order': 0
            }
        )
        categories[category.name] = category
        if created:
            print(f"Created category: {category.name}")
    
    # Create sample products
    products_data = [
        # Rolex Watches
        {'name': 'Rolex Submariner Date', 'brand': 'Rolex', 'category': 'Luxury Watches', 'price': 9550, 'description': 'Iconic diving watch with date display'},
        {'name': 'Rolex GMT-Master II', 'brand': 'Rolex', 'category': 'Men\'s Watches', 'price': 10700, 'description': 'Professional pilot watch with dual time zone'},
        {'name': 'Rolex Datejust 36', 'brand': 'Rolex', 'category': 'Luxury Watches', 'price': 7650, 'description': 'Classic dress watch with date function'},
        {'name': 'Rolex Daytona', 'brand': 'Rolex', 'category': 'Men\'s Watches', 'price': 14800, 'description': 'Racing chronograph watch'},
        {'name': 'Rolex Lady-Datejust', 'brand': 'Rolex', 'category': 'Women\'s Watches', 'price': 6850, 'description': 'Elegant ladies watch'},
        
        # Patek Philippe Watches
        {'name': 'Patek Philippe Calatrava', 'brand': 'Patek Philippe', 'category': 'Luxury Watches', 'price': 32400, 'description': 'Classic dress watch epitome'},
        {'name': 'Patek Philippe Nautilus', 'brand': 'Patek Philippe', 'category': 'Men\'s Watches', 'price': 81500, 'description': 'Luxury sports watch'},
        {'name': 'Patek Philippe Aquanaut', 'brand': 'Patek Philippe', 'category': 'Luxury Watches', 'price': 42200, 'description': 'Modern sports watch'},
        {'name': 'Patek Philippe World Time', 'brand': 'Patek Philippe', 'category': 'Men\'s Watches', 'price': 69800, 'description': 'World time complications'},
        
        # Omega Watches
        {'name': 'Omega Speedmaster Professional', 'brand': 'Omega', 'category': 'Men\'s Watches', 'price': 6350, 'description': 'Moonwatch chronograph'},
        {'name': 'Omega Seamaster Planet Ocean', 'brand': 'Omega', 'category': 'Luxury Watches', 'price': 7200, 'description': 'Professional diving watch'},
        {'name': 'Omega Constellation Manhattan', 'brand': 'Omega', 'category': 'Women\'s Watches', 'price': 4850, 'description': 'Elegant ladies timepiece'},
        {'name': 'Omega De Ville Prestige', 'brand': 'Omega', 'category': 'Luxury Watches', 'price': 3950, 'description': 'Classic dress watch'},
        
        # Cartier Jewelry
        {'name': 'Cartier Love Ring', 'brand': 'Cartier', 'category': 'Rings', 'price': 1750, 'description': 'Iconic screw motif ring'},
        {'name': 'Cartier Juste un Clou Necklace', 'brand': 'Cartier', 'category': 'Necklaces', 'price': 2890, 'description': 'Nail-inspired necklace'},
        {'name': 'Cartier Trinity Ring', 'brand': 'Cartier', 'category': 'Rings', 'price': 2150, 'description': 'Three-band rolling ring'},
        {'name': 'Cartier Panthere Ring', 'brand': 'Cartier', 'category': 'Rings', 'price': 8450, 'description': 'Panther-inspired ring'},
        
        # Tiffany & Co. Jewelry
        {'name': 'Tiffany Setting Engagement Ring', 'brand': 'Tiffany & Co.', 'category': 'Rings', 'price': 12800, 'description': 'Classic solitaire engagement ring'},
        {'name': 'Tiffany T1 Wide Ring', 'brand': 'Tiffany & Co.', 'category': 'Rings', 'price': 3650, 'description': 'Modern T collection ring'},
        {'name': 'Tiffany Return to Heart Necklace', 'brand': 'Tiffany & Co.', 'category': 'Necklaces', 'price': 1950, 'description': 'Heart-shaped pendant necklace'},
        {'name': 'Tiffany Atlas Ring', 'brand': 'Tiffany & Co.', 'category': 'Rings', 'price': 2750, 'description': 'Roman numeral ring'},
        
        # Bulgari Jewelry
        {'name': 'Bulgari Serpenti Ring', 'brand': 'Bulgari', 'category': 'Rings', 'price': 4250, 'description': 'Snake-inspired ring'},
        {'name': 'Bulgari B.zero1 Necklace', 'brand': 'Bulgari', 'category': 'Necklaces', 'price': 3150, 'description': 'Spiral design necklace'},
        {'name': 'Bulgari Divas\' Dream Ring', 'brand': 'Bulgari', 'category': 'Rings', 'price': 5850, 'description': 'Fan-inspired ring'},
        {'name': 'Bulgari Parentesi Necklace', 'brand': 'Bulgari', 'category': 'Necklaces', 'price': 2650, 'description': 'Architectural inspired necklace'},
        
        # Additional products to test pagination
        {'name': 'Omega Speedmaster Racing', 'brand': 'Omega', 'category': 'Men\'s Watches', 'price': 5950, 'description': 'Racing-inspired chronograph'},
        {'name': 'Rolex Explorer II', 'brand': 'Rolex', 'category': 'Men\'s Watches', 'price': 8550, 'description': 'Cave explorer watch'},
        {'name': 'Cartier Santos', 'brand': 'Cartier', 'category': 'Luxury Watches', 'price': 7300, 'description': 'Aviation-inspired watch'},
        {'name': 'Tiffany Atlas Watch', 'brand': 'Tiffany & Co.', 'category': 'Women\'s Watches', 'price': 4200, 'description': 'Roman numeral watch'},
        {'name': 'Bulgari Octo Finissimo', 'brand': 'Bulgari', 'category': 'Men\'s Watches', 'price': 19800, 'description': 'Ultra-thin luxury watch'},
        {'name': 'Patek Philippe Twenty~4', 'brand': 'Patek Philippe', 'category': 'Women\'s Watches', 'price': 15600, 'description': 'Ladies rectangular watch'},
    ]
    
    created_count = 0
    for product_data in products_data:
        try:
            product, created = Product.objects.get_or_create(
                name=product_data['name'],
                defaults={
                    'brand': brands[product_data['brand']],
                    'category': categories[product_data['category']],
                    'price': Decimal(str(product_data['price'])),
                    'description': product_data['description'],
                    'is_active': True,
                    'show_on_homepage': created_count < 8,  # Show first 8 on homepage
                    'stock_quantity': 10,
                    'sku': f"SKU-{slugify(product_data['name'])[:10].upper()}"
                }
            )
            
            if created:
                created_count += 1
                print(f"Created product: {product.name} - ${product.price}")
        except Exception as e:
            print(f"Error creating product {product_data['name']}: {e}")
    
    print(f"\nTotal products created: {created_count}")
    print(f"Total products in database: {Product.objects.count()}")
    print("\nSample data creation completed!")

if __name__ == '__main__':
    create_sample_data()
