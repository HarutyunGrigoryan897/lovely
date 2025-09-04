#!/usr/bin/env python3
"""
Script to add test additional images to existing products for testing the image gallery
"""
import os
import sys
import django

# Setup Django environment
sys.path.append('/Users/harutyungrigoryan/Desktop/lovely/web_app')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from shop.models import Product, ProductImage
from django.core.files.uploadedfile import SimpleUploadedFile
import shutil

def add_test_images():
    """Add some test additional images to products"""
    # Get some products to add images to
    products = Product.objects.all()[:3]  # First 3 products
    
    # List of existing images in media folder we can reuse
    existing_images = [
        '81hUA9xKNuL._UF8941000_QL80_.jpg',
        # Add more existing image names here if they exist
    ]
    
    for i, product in enumerate(products):
        print(f"Adding additional images to: {product.name}")
        
        # Delete existing additional images for clean test
        product.additional_images.all().delete()
        
        # Try to add some test images by copying the main product image
        # with different names/sort orders
        if product.image:
            for j in range(2):  # Add 2 additional images per product
                try:
                    # Create a ProductImage instance
                    additional_image = ProductImage.objects.create(
                        product=product,
                        alt_text=f"{product.name} - View {j+2}",
                        sort_order=j+1
                    )
                    
                    # Copy the main image file to create a "different" image
                    # In a real scenario, these would be different actual images
                    source_path = product.image.path
                    if os.path.exists(source_path):
                        # Create new filename
                        base_name = os.path.splitext(os.path.basename(source_path))[0]
                        extension = os.path.splitext(source_path)[1]
                        new_filename = f"{base_name}_view_{j+2}{extension}"
                        
                        # Copy file to gallery folder
                        gallery_dir = os.path.join(os.path.dirname(source_path), 'gallery')
                        os.makedirs(gallery_dir, exist_ok=True)
                        new_path = os.path.join(gallery_dir, new_filename)
                        
                        shutil.copy2(source_path, new_path)
                        
                        # Update the image field
                        additional_image.image.name = f'products/gallery/{new_filename}'
                        additional_image.save()
                        
                        print(f"  Added additional image: {new_filename}")
                        
                except Exception as e:
                    print(f"  Error adding image {j+1}: {e}")

if __name__ == "__main__":
    add_test_images()
    print("Test images added successfully!")
