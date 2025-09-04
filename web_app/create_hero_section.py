#!/usr/bin/env python
import os
import sys
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from shop.models import HeroSection

def create_hero_section():
    """Create a default hero section"""
    
    # Check if any hero section already exists
    if HeroSection.objects.exists():
        print("Hero section already exists!")
        return
    
    # Create a default hero section
    hero = HeroSection.objects.create(
        title="Teluxe",
        subtitle="Discover the finest luxury timepieces from the world's most prestigious brands",
        button_text="Explore Collection",
        button_url="/catalog/",
        is_active=True
    )
    
    print(f"Created hero section: {hero.title}")
    print(f"Subtitle: {hero.subtitle}")
    print(f"Button: {hero.button_text} -> {hero.button_url}")
    print("Hero section created successfully!")

if __name__ == '__main__':
    create_hero_section()
