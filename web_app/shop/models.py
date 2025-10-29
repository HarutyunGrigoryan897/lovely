from django.db import models
from django.utils.text import slugify
from django.core.validators import MinValueValidator, MaxValueValidator
from decimal import Decimal
from django.contrib.auth import get_user_model

User = get_user_model()


class GoldPrice(models.Model):
    """Gold price per gram configuration"""
    price_per_gram = models.DecimalField(max_digits=10, decimal_places=2, help_text="Price per gram in USD")
    is_active = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Gold Price'
        verbose_name_plural = 'Gold Prices'

    def __str__(self):
        return f"${self.price_per_gram}/gram - {'Active' if self.is_active else 'Inactive'}"

    @classmethod
    def get_current_price(cls):
        """Get the current active gold price"""
        active_price = cls.objects.filter(is_active=True).first()
        if active_price:
            # Apply markup
            base_price = active_price.price_per_gram
            return base_price
        return Decimal('0.00')


class DiamondPrice(models.Model):
    """Diamond pricing - Price per unit for each size range"""
    DIAMOND_TYPE_CHOICES = [
        ('natural', 'Natural Diamond'),
        ('lab', 'Lab Diamond'),
    ]
    
    SIZE_CHOICES = [
        ('under_5', 'Under 5'),
        ('5_to_7', '5 to 7'),
        ('8_to_12', '8 to 12'),
        ('13_to_17', '13 to 17'),
    ]
    
    diamond_type = models.CharField(max_length=20, choices=DIAMOND_TYPE_CHOICES)
    size_category = models.CharField(max_length=20, choices=SIZE_CHOICES)
    price_per_unit = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, help_text="Price per unit - will be multiplied by user's quantity")

    class Meta:
        ordering = ['diamond_type', 'size_category']
        verbose_name = 'Diamond Price'
        verbose_name_plural = 'Diamond Prices'
        unique_together = ['diamond_type', 'size_category']

    def __str__(self):
        return f"{self.diamond_type} ----- {self.size_category}"


class WorkPrice(models.Model):
    """Work/labor price configuration"""
    price = models.DecimalField(max_digits=10, decimal_places=2, default=7000.00, help_text="Work price in USD")
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Work Price'
        verbose_name_plural = 'Work Prices'

    def __str__(self):
        return f"Work Price: ${self.price}"

    @classmethod
    def get_current_price(cls):
        """Get the current active work price"""
        active_price = cls.objects.all().first()
        return active_price.price if active_price else Decimal('7000.00')


class ShippingAddress(models.Model):
    """User's saved shipping addresses"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='shipping_addresses')
    label = models.CharField(max_length=50, help_text="e.g., Home, Work, Office")
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=20, blank=True, null=True)
    country = models.CharField(max_length=100)
    is_default = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-is_default', '-created_at']
        verbose_name = 'Shipping Address'
        verbose_name_plural = 'Shipping Addresses'

    def __str__(self):
        return f"{self.label} - {self.first_name} {self.last_name}, {self.city}, {self.country}"

    def save(self, *args, **kwargs):
        # If this is set as default, remove default from other addresses
        if self.is_default:
            ShippingAddress.objects.filter(user=self.user, is_default=True).exclude(pk=self.pk).update(is_default=False)
        super().save(*args, **kwargs)


class Brand(models.Model):
    """Luxury brand model for watches and jewelry"""
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    description = models.TextField(blank=True)
    logo = models.ImageField(upload_to='brands/', blank=True, null=True)
    show_on_homepage = models.BooleanField(default=False, help_text="Display this brand on the homepage")

    class Meta:
        ordering = ['name']
        verbose_name = 'Brand'
        verbose_name_plural = 'Brands'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Category(models.Model):
    """Product categories (Watches, Jewelry, etc.)"""
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='categories/', blank=True, null=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True, related_name='subcategories')
    is_active = models.BooleanField(default=True)
    sort_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['sort_order', 'name']
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Product(models.Model):
    """Main product model for luxury items"""
    STOCK_STATUS_CHOICES = [
        ('in_stock', 'In Stock'),
        ('limited', 'Limited Stock'),
        ('pre_order', 'Pre-Order'),
        ('out_of_stock', 'Out of Stock'),
    ]

    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name='products')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    description = models.TextField()
    short_description = models.CharField(max_length=500, blank=True)
    
    # Pricing - DEPRECATED: Price is now calculated from gold_weight_grams
    # Keeping these fields for backward compatibility but they are no longer used
    # The actual price is calculated via display_price property
    original_price = models.DecimalField(
        max_digits=12, 
        decimal_places=2, 
        blank=True, 
        null=True,
        help_text='DEPRECATED: Not used. Price is calculated from gold weight.'
    )
    cost_price = models.DecimalField(
        max_digits=12, 
        decimal_places=2, 
        blank=True, 
        null=True,
        help_text='Internal cost tracking only'
    )
    markup_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=25.00, help_text="Markup percentage (default 25%)")

    # Images
    image = models.ImageField(upload_to='products/')
    image_alt = models.CharField(max_length=200, blank=True)
    
    # Stock management
    stock_status = models.CharField(max_length=20, choices=STOCK_STATUS_CHOICES, default='in_stock')
    stock_quantity = models.PositiveIntegerField(default=0)
    low_stock_threshold = models.PositiveIntegerField(default=5)
    
    # Product details
    sku = models.CharField(max_length=50, unique=True, blank=True)
    model_number = models.CharField(max_length=100, blank=True)
    year_released = models.PositiveIntegerField(blank=True, null=True)
    
    # Gold and Diamond specifications
    gold_weight_grams = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        default=0,
        validators=[MinValueValidator(Decimal('0.00'))],
        help_text="Weight of gold in grams"
    )
    has_diamonds = models.BooleanField(default=False, help_text="Does this product include diamonds?")
    diamond_size = models.CharField(
        max_length=20,
        choices=[
            ('under_5', 'Under 5'),
            ('5_to_7', '5 to 7'),
            ('8_to_12', '8 to 12'),
            ('13_to_17', '13 to 17'),
        ],
        blank=True,
        null=True,
        help_text="Size category of diamonds for this product"
    )
    diamond_carats = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        validators=[MinValueValidator(Decimal('0.00'))],
        help_text="Total carats of diamonds in this product",
        blank=True, null=True
    )
    
    # SEO
    meta_title = models.CharField(max_length=60, blank=True)
    meta_description = models.CharField(max_length=160, blank=True)
    meta_keywords = models.CharField(max_length=255, blank=True)
    
    # Status and timestamps
    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    show_on_homepage = models.BooleanField(default=False, help_text="Display this product on the homepage")
    is_limited_edition = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Product'
        verbose_name_plural = 'Products'
        indexes = [
            models.Index(fields=['slug']),
            models.Index(fields=['brand', 'category']),
            models.Index(fields=['is_active', 'stock_status']),
        ]

    def __str__(self):
        return f"{self.brand.name} - {self.name}"

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(f"{self.brand.name} {self.name}")
            slug = base_slug
            counter = 1
            while Product.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        
        # Auto-generate SKU only if not manually provided
        if not self.sku:
            # First save to get ID if creating new product
            if not self.id:
                super().save(*args, **kwargs)
            
            # Generate SKU with actual ID
            base_sku = f"{self.brand.name[:3].upper()}-{self.id}-{slugify(self.name)[:10].upper()}"
            
            # Ensure SKU is unique (shouldn't happen but just in case)
            sku = base_sku
            counter = 1
            while Product.objects.filter(sku=sku).exclude(id=self.id).exists():
                sku = f"{base_sku}-{counter}"
                counter += 1
            
            self.sku = sku
        
        super().save(*args, **kwargs)

    @property
    def is_on_sale(self):
        return self.original_price and self.original_price > self.price

    @property
    def discount_percentage(self):
        if self.is_on_sale:
            return round(((self.original_price - self.price) / self.original_price) * 100)
        return 0

    @property
    def is_low_stock(self):
        return self.stock_quantity <= self.low_stock_threshold

    def calculate_gold_price(self):
        """
        Calculate the price of gold in this product
        Formula: (gold_weight_grams * price_per_gram * 0.76) + markup_percentage
        """
        if self.gold_weight_grams > 0:
            gold_price_per_gram = GoldPrice.get_current_price()
            # Apply standard 0.76 multiplier
            base_gold_price = self.gold_weight_grams * gold_price_per_gram * Decimal('0.76')
            # Add markup percentage
            markup_amount = base_gold_price * (self.markup_percentage / Decimal('100'))
            total_gold_price = base_gold_price + markup_amount
            return total_gold_price
        return Decimal('0.00')
    
    def get_display_price(self, user=None, size_multiplier=None, diamond_type=None):
        """
        PRIMARY PRICE - Always calculated from gold + work + diamonds (if applicable)
        Formula: (gold_price + work_price + diamond_price) * size_multiplier * user_level_multiplier
        
        Args:
            user: User object to apply level multiplier
            size_multiplier: Decimal for size-based price adjustment (default 1.0)
            diamond_type: 'natural' or 'lab' if product has diamonds
        
        Returns:
            Decimal: Final calculated price
        """
        # Calculate gold price (already includes 0.76 multiplier and markup)
        gold_price = self.calculate_gold_price()
        
        # Add work price
        work_price = WorkPrice.get_current_price()
        
        # Calculate diamond price if applicable
        diamond_price = Decimal('0.00')
        if self.has_diamonds and diamond_type and self.diamond_size and self.diamond_carats > 0:
            try:
                diamond_pricing = DiamondPrice.objects.get(
                    diamond_type=diamond_type,
                    size_category=self.diamond_size
                )
                # Price per unit * carats
                diamond_price = diamond_pricing.price_per_unit * self.diamond_carats
            except DiamondPrice.DoesNotExist:
                pass
        
        # Base price: gold + work + diamonds
        base_price = gold_price + work_price + diamond_price
        
        # Apply size multiplier (default to 1.0 if not provided)
        if size_multiplier is None:
            size_multiplier = Decimal('1.0')
        base_price = base_price * size_multiplier
        
        # Apply user level multiplier
        if user and hasattr(user, 'get_price_multiplier'):
            multiplier = user.get_price_multiplier()
            base_price = base_price * multiplier
        
        return base_price
    
    @property
    def display_price(self):
        """
        Backward compatibility - returns base price without user multiplier
        Use get_display_price(user) for user-specific pricing
        """
        return self.get_display_price()
    
    @property
    def base_price(self):
        """Alias for display_price - for backward compatibility"""
        return self.display_price
    
    @property
    def price(self):
        """Backward compatibility - returns calculated price"""
        return self.display_price

    def calculate_base_price(self, diamond_type=None, user=None, size_multiplier=None):
        """
        Calculate total price with breakdown: gold + diamonds + work
        Formula: (gold_price + work_price + diamond_price) * size_multiplier * user_level_multiplier
        
        Args:
            diamond_type: 'natural' or 'lab' - user chooses the type
            user: User object to apply level multiplier
            size_multiplier: Decimal for size-based price adjustment (default 1.0)
        
        Returns:
            dict: Breakdown of prices and total
        """
        # Calculate gold price (already includes 0.76 multiplier and markup)
        gold_price = self.calculate_gold_price()
        
        # Calculate diamond price - based on product's predefined size and carats
        diamond_price = Decimal('0.00')
        if self.has_diamonds and diamond_type and self.diamond_size and self.diamond_carats > 0:
            try:
                diamond_pricing = DiamondPrice.objects.get(
                    diamond_type=diamond_type,
                    size_category=self.diamond_size
                )
                # Price per unit * carats
                diamond_price = diamond_pricing.price_per_unit * self.diamond_carats
            except DiamondPrice.DoesNotExist:
                pass
        
        # Work price
        work_price = WorkPrice.get_current_price()
        
        # Base total before multipliers
        base_total = gold_price + diamond_price + work_price
        
        # Apply size multiplier (default to 1.0 if not provided)
        if size_multiplier is None:
            size_multiplier = Decimal('1.0')
        
        # Apply size multiplier to all components
        gold_price = gold_price * size_multiplier
        diamond_price = diamond_price * size_multiplier
        work_price = work_price * size_multiplier
        total = base_total * size_multiplier
        
        # Apply user level multiplier
        if user and hasattr(user, 'get_price_multiplier'):
            multiplier = user.get_price_multiplier()
            gold_price = gold_price * multiplier
            diamond_price = diamond_price * multiplier
            work_price = work_price * multiplier
            total = total * multiplier
        
        return {
            'gold_price': gold_price,
            'diamond_price': diamond_price,
            'work_price': work_price,
            'total_price': total
        }


class ProductImage(models.Model):
    """Additional product images"""
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='additional_images')
    image = models.ImageField(upload_to='products/gallery/')
    alt_text = models.CharField(max_length=200, blank=True)
    is_primary = models.BooleanField(default=False)
    sort_order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['sort_order']
        verbose_name = 'Product Image'
        verbose_name_plural = 'Product Images'

    def __str__(self):
        return f"{self.product.name} - Image {self.sort_order}"


class ProductSize(models.Model):
    """Product size options with price multipliers"""
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='sizes')
    size_label = models.CharField(max_length=50, help_text="Size label (e.g., 17mm, 19mm, 42mm, S, M, L, etc.)")
    price_multiplier = models.DecimalField(
        max_digits=5, 
        decimal_places=2, 
        default=1.00,
        validators=[MinValueValidator(Decimal('0.01'))],
        help_text="Price multiplier for this size (e.g., 1.0 = base price, 1.2 = 20% more)"
    )
    is_default = models.BooleanField(default=False, help_text="Is this the default size?")
    sort_order = models.PositiveIntegerField(default=0, help_text="Display order")
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['product', 'sort_order']
        verbose_name = 'Product Size'
        verbose_name_plural = 'Product Sizes'
        unique_together = ['product', 'size_label']

    def __str__(self):
        return f"{self.product.name} - {self.size_label} (×{self.price_multiplier})"

    def save(self, *args, **kwargs):
        # If this is set as default, remove default from other sizes for this product
        if self.is_default:
            ProductSize.objects.filter(product=self.product, is_default=True).exclude(pk=self.pk).update(is_default=False)
        super().save(*args, **kwargs)


class ProductDiamondOption(models.Model):
    """Default diamond configuration for a product"""
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='diamond_options')
    size_category = models.CharField(
        max_length=20,
        choices=[
            ('under_5', 'Under 5 (2.22mm)'),
            ('5_to_7', '5 to 7 (3.57mm)'),
            ('8_to_12', '8 to 12 (1.85mm)'),
            ('13_to_17', '13 to 17 (0.16mm)'),
        ]
    )
    default_quantity = models.IntegerField(default=0, help_text="Default quantity for this size")
    min_quantity = models.IntegerField(default=0, help_text="Minimum quantity allowed")
    max_quantity = models.IntegerField(default=1000, help_text="Maximum quantity allowed")
    
    class Meta:
        unique_together = ['product', 'size_category']
        ordering = ['size_category']
        verbose_name = 'Product Diamond Option'
        verbose_name_plural = 'Product Diamond Options'
    
    def __str__(self):
        return f"{self.product.name} - {self.get_size_category_display()}: {self.default_quantity} diamonds"


class WatchSpecification(models.Model):
    """Detailed specifications for watches"""
    CASE_MATERIAL_CHOICES = [
        ('stainless_steel', 'Stainless Steel'),
        ('gold', 'Gold'),
        ('rose_gold', 'Rose Gold'),
        ('white_gold', 'White Gold'),
        ('platinum', 'Platinum'),
        ('titanium', 'Titanium'),
        ('ceramic', 'Ceramic'),
        ('carbon_fiber', 'Carbon Fiber'),
        ('bronze', 'Bronze'),
        ('aluminum', 'Aluminum'),
    ]

    MOVEMENT_CHOICES = [
        ('automatic', 'Automatic'),
        ('manual', 'Manual'),
        ('quartz', 'Quartz'),
        ('chronograph', 'Chronograph'),
        ('smartwatch', 'Smartwatch'),
        ('solar', 'Solar'),
        ('kinetic', 'Kinetic'),
    ]

    CRYSTAL_CHOICES = [
        ('sapphire', 'Sapphire Crystal'),
        ('mineral', 'Mineral Crystal'),
        ('acrylic', 'Acrylic'),
        ('gorilla_glass', 'Gorilla Glass'),
    ]

    product = models.OneToOneField(Product, on_delete=models.CASCADE, related_name='watch_specs')
    
    # Case specifications
    case_material = models.CharField(max_length=20, choices=CASE_MATERIAL_CHOICES)
    case_size = models.CharField(max_length=20, help_text="e.g., 42mm, 40mm")
    case_thickness = models.CharField(max_length=20, blank=True, help_text="e.g., 12mm")
    case_shape = models.CharField(max_length=50, blank=True, help_text="e.g., Round, Square, Tonneau")
    
    # Movement specifications
    movement = models.CharField(max_length=20, choices=MOVEMENT_CHOICES)
    movement_caliber = models.CharField(max_length=100, blank=True, help_text="e.g., Cal. 3135")
    power_reserve = models.CharField(max_length=50, blank=True, help_text="e.g., 48 hours")
    jewels = models.PositiveIntegerField(blank=True, null=True)
    frequency = models.CharField(max_length=50, blank=True, help_text="e.g., 28,800 vph")
    
    # Dial and display
    dial_color = models.CharField(max_length=50, blank=True)
    dial_material = models.CharField(max_length=100, blank=True)
    hands_style = models.CharField(max_length=100, blank=True)
    markers_type = models.CharField(max_length=100, blank=True)
    complications = models.TextField(blank=True, help_text="Date, GMT, Chronograph, etc.")
    
    # Crystal and protection
    crystal_type = models.CharField(max_length=20, choices=CRYSTAL_CHOICES, blank=True)
    water_resistance = models.CharField(max_length=50, help_text="e.g., 100m, 300m")
    
    # Bracelet/Strap
    bracelet_material = models.CharField(max_length=100, blank=True)
    bracelet_color = models.CharField(max_length=50, blank=True)
    clasp_type = models.CharField(max_length=100, blank=True)
    lug_width = models.CharField(max_length=20, blank=True, help_text="e.g., 20mm")
    
    # Additional features
    bezel_type = models.CharField(max_length=100, blank=True)
    bezel_material = models.CharField(max_length=100, blank=True)
    crown_type = models.CharField(max_length=100, blank=True)
    
    # Certifications
    certifications = models.TextField(blank=True, help_text="COSC, Master Chronometer, etc.")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Watch Specification'
        verbose_name_plural = 'Watch Specifications'

    def __str__(self):
        return f"{self.product.name} - Watch Specs"


class JewelrySpecification(models.Model):
    """Detailed specifications for jewelry"""
    JEWELRY_TYPE_CHOICES = [
        ('ring', 'Ring'),
        ('necklace', 'Necklace'),
        ('bracelet', 'Bracelet'),
        ('earrings', 'Earrings'),
        ('pendant', 'Pendant'),
        ('brooch', 'Brooch'),
        ('cufflinks', 'Cufflinks'),
        ('anklet', 'Anklet'),
    ]

    METAL_TYPE_CHOICES = [
        ('gold_14k', '14K Gold'),
        ('gold_18k', '18K Gold'),
        ('gold_24k', '24K Gold'),
        ('white_gold', 'White Gold'),
        ('rose_gold', 'Rose Gold'),
        ('platinum', 'Platinum'),
        ('silver', 'Sterling Silver'),
        ('titanium', 'Titanium'),
        ('stainless_steel', 'Stainless Steel'),
    ]

    GEMSTONE_CHOICES = [
        ('diamond', 'Diamond'),
        ('ruby', 'Ruby'),
        ('sapphire', 'Sapphire'),
        ('emerald', 'Emerald'),
        ('pearl', 'Pearl'),
        ('opal', 'Opal'),
        ('topaz', 'Topaz'),
        ('amethyst', 'Amethyst'),
        ('garnet', 'Garnet'),
        ('turquoise', 'Turquoise'),
    ]

    product = models.OneToOneField(Product, on_delete=models.CASCADE, related_name='jewelry_specs')
    
    # Basic jewelry info
    jewelry_type = models.CharField(max_length=20, choices=JEWELRY_TYPE_CHOICES)
    metal_type = models.CharField(max_length=20, choices=METAL_TYPE_CHOICES)
    metal_purity = models.CharField(max_length=20, blank=True, help_text="e.g., 750, 925")
    metal_weight = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True, help_text="Weight in grams")
    
    # Gemstone information
    has_gemstones = models.BooleanField(default=False)
    primary_gemstone = models.CharField(max_length=20, choices=GEMSTONE_CHOICES, blank=True)
    gemstone_carat = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    gemstone_clarity = models.CharField(max_length=50, blank=True, help_text="e.g., VS1, VVS2")
    gemstone_color = models.CharField(max_length=50, blank=True)
    gemstone_cut = models.CharField(max_length=50, blank=True, help_text="e.g., Round, Princess, Emerald")
    stone_count = models.PositiveIntegerField(blank=True, null=True)
    
    # Dimensions
    length = models.CharField(max_length=50, blank=True, help_text="Overall length")
    width = models.CharField(max_length=50, blank=True, help_text="Overall width")
    thickness = models.CharField(max_length=50, blank=True, help_text="Thickness/height")
    
    # Specific measurements for different jewelry types
    ring_size = models.CharField(max_length=20, blank=True, help_text="Ring size if applicable")
    chain_length = models.CharField(max_length=20, blank=True, help_text="Chain length if applicable")
    pendant_dimensions = models.CharField(max_length=100, blank=True)
    
    # Design details
    style = models.CharField(max_length=100, blank=True, help_text="e.g., Vintage, Modern, Art Deco")
    finish = models.CharField(max_length=100, blank=True, help_text="e.g., Polished, Brushed, Matte")
    setting_type = models.CharField(max_length=100, blank=True, help_text="e.g., Prong, Bezel, Pave")
    
    # Care instructions
    care_instructions = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Jewelry Specification'
        verbose_name_plural = 'Jewelry Specifications'

    def __str__(self):
        return f"{self.product.name} - Jewelry Specs"


class ProductCustomization(models.Model):
    """Customization options for products"""
    CUSTOMIZATION_TYPE_CHOICES = [
        ('engraving', 'Engraving'),
        ('band_color', 'Band Color'),
        ('case_material', 'Case Material'),
        ('dial_color', 'Dial Color'),
        ('gemstone', 'Gemstone'),
        ('metal_type', 'Metal Type'),
        ('size', 'Size'),
        ('length', 'Length'),
    ]

    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='customizations')
    customization_type = models.CharField(max_length=20, choices=CUSTOMIZATION_TYPE_CHOICES)
    name = models.CharField(max_length=100, help_text="Display name for this option")
    value = models.CharField(max_length=100, help_text="Internal value for this option")
    description = models.TextField(blank=True)
    price_modifier = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, help_text="Additional cost for this option")
    is_available = models.BooleanField(default=True)
    sort_order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['customization_type', 'sort_order']
        verbose_name = 'Product Customization'
        verbose_name_plural = 'Product Customizations'
        unique_together = ['product', 'customization_type', 'value']

    def __str__(self):
        return f"{self.product.name} - {self.get_customization_type_display()}: {self.name}"


class Cart(models.Model):
    """Shopping cart for users"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='cart')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Shopping Cart'
        verbose_name_plural = 'Shopping Carts'

    def __str__(self):
        return f"Cart for {self.user.username or self.user.telegram_id}"

    @property
    def total_items(self):
        """Total number of items in cart"""
        return self.items.aggregate(
            total=models.Sum('quantity')
        )['total'] or 0

    @property
    def total_price(self):
        """Total price of all items in cart"""
        total = Decimal('0.00')
        for item in self.items.all():
            total += item.total_price
        return total

    @property
    def item_count(self):
        """Number of different items in cart"""
        return self.items.count()

    def clear(self):
        """Remove all items from cart"""
        self.items.all().delete()


class CartItem(models.Model):
    """Individual items in a shopping cart"""
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)])
    
    # Store customization details
    customization_data = models.JSONField(blank=True, null=True, help_text="Store product customization options")
    customization_price = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    
    # Store the price at the time of adding to cart
    unit_price = models.DecimalField(max_digits=12, decimal_places=2)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['cart', 'product', 'customization_data']
        verbose_name = 'Cart Item'
        verbose_name_plural = 'Cart Items'
        ordering = ['-created_at']

    def __str__(self):
        customization_info = ""
        if self.customization_data:
            customization_info = f" (Customized)"
        return f"{self.quantity}x {self.product.name}{customization_info}"

    def save(self, *args, **kwargs):
        # Store the current product price when adding to cart
        if not self.unit_price:
            user = self.cart.user
            
            # Extract size multiplier and diamond type from customization data
            size_multiplier = Decimal('1.0')
            diamond_type = None
            
            if self.customization_data:
                # Check for size selection
                if 'size' in self.customization_data:
                    size_label = self.customization_data['size']
                    try:
                        from .models import ProductSize
                        product_size = ProductSize.objects.get(
                            product=self.product,
                            size_label=size_label
                        )
                        size_multiplier = product_size.price_multiplier
                    except ProductSize.DoesNotExist:
                        pass
                
                # Check for diamond type selection
                if 'diamond_type' in self.customization_data:
                    diamond_type = self.customization_data['diamond_type']
            
            # Calculate price with all multipliers
            self.unit_price = self.product.get_display_price(
                user=user,
                size_multiplier=size_multiplier,
                diamond_type=diamond_type
            )
        super().save(*args, **kwargs)

    @property
    def total_price(self):
        """Total price for this cart item including customizations"""
        # Unit price already includes user multiplier from save()
        return (self.unit_price + self.customization_price) * self.quantity

    @property
    def customized_product_name(self):
        """Get product name with customization details"""
        if not self.customization_data:
            return self.product.name
        
        name = self.product.name
        customizations = []
        
        # Handle diamond specifications format
        if isinstance(self.customization_data, dict):
            if 'diamond_type' in self.customization_data:
                # This is a diamond specification
                diamond_type = self.customization_data.get('diamond_type', 'natural')
                customizations.append(f"{diamond_type.capitalize()} Diamonds")
                return f"{name} ({', '.join(customizations)})"
            
            # Handle other customization types
            for key, value in self.customization_data.items():
                if value and value != 'None' and not isinstance(value, (dict, list)):
                    # Format customization display
                    if key == 'band_color':
                        customizations.append(f"{value} Band")
                    elif key == 'dial_color':
                        customizations.append(f"{value} Dial")
                    elif key == 'engraving':
                        customizations.append(f"with {value}")
                    elif key == 'size':
                        customizations.append(f"{value}")
                    elif key not in ['diamond_quantities', 'gold_price', 'diamond_price', 'work_price']:
                        customizations.append(str(value))
        
        if customizations:
            name += f" ({', '.join(customizations)})"
        
        return name


class Order(models.Model):
    """Customer order model"""
    ORDER_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    order_number = models.CharField(max_length=20, unique=True)
    status = models.CharField(max_length=20, choices=ORDER_STATUS_CHOICES, default='pending')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    total_items = models.PositiveIntegerField()
    
    # Customer information (in case user updates their profile later)
    customer_email = models.EmailField()
    customer_first_name = models.CharField(max_length=100, blank=True, default='')
    customer_last_name = models.CharField(max_length=100, blank=True, default='')
    
    # Reference to shipping address (for new orders)
    shipping_address_ref = models.ForeignKey(ShippingAddress, on_delete=models.SET_NULL, null=True, blank=True, related_name='orders')
    
    # Shipping information snapshot (kept for historical orders)
    shipping_first_name = models.CharField(max_length=100, blank=True, default='')
    shipping_last_name = models.CharField(max_length=100, blank=True, default='')
    shipping_address = models.CharField(max_length=255, blank=True, default='')
    shipping_city = models.CharField(max_length=100, blank=True, default='')
    shipping_zip_code = models.CharField(max_length=20, blank=True, default='')
    shipping_country = models.CharField(max_length=100, blank=True, default='')
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'
    
    def __str__(self):
        return f"Order {self.order_number} - {self.user.username}"
    
    def save(self, *args, **kwargs):
        if not self.order_number:
            import uuid
            from datetime import datetime
            # Generate order number: ORD-YYYYMMDD-XXXX
            date_part = datetime.now().strftime('%Y%m%d')
            unique_part = str(uuid.uuid4())[:8].upper()
            self.order_number = f"ORD-{date_part}-{unique_part}"
        super().save(*args, **kwargs)


class OrderItem(models.Model):
    """Individual items in an order"""
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Price at time of order
    customization_data = models.JSONField(null=True, blank=True)  # Store customization details
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Order Item'
        verbose_name_plural = 'Order Items'
    
    def __str__(self):
        customizations = ""
        if self.customization_data:
            try:
                data = self.customization_data if isinstance(self.customization_data, dict) else {}
                customizations = f" ({', '.join(f'{k}: {v}' for k, v in data.items())})"
            except:
                pass
        return f"{self.product.name}{customizations} x{self.quantity}"
    
    @property
    def total_price(self):
        return self.price * self.quantity


class HeroSection(models.Model):
    """Homepage hero section content"""
    title = models.CharField(max_length=100, default="Teluxe")
    subtitle = models.CharField(max_length=200, default="Discover the finest luxury timepieces from the world's most prestigious brands")
    background_image = models.ImageField(upload_to='hero/', help_text="High-quality hero background image")
    button_text = models.CharField(max_length=50, default="Explore Collection")
    button_url = models.CharField(max_length=200, default="/catalog/", help_text="URL the button should link to")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Hero Section'
        verbose_name_plural = 'Hero Sections'
        ordering = ['-created_at']

    def __str__(self):
        return f"Hero: {self.title}"

    @classmethod
    def get_active_hero(cls):
        """Get the currently active hero section"""
        return cls.objects.filter(is_active=True).first()