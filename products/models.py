from decimal import Decimal
from django.db import models
from django.contrib.auth.models import User


CATEGORY_CHOICES = [
    ('electronics', 'Electronics'),
    ('fashion', 'Fashion'),
    ('home', 'Home & Kitchen'),
    ('sports', 'Sports & Fitness'),
    ('books', 'Books'),
    ('accessories', 'Accessories'),
    ('beauty', 'Beauty & Personal Care'),
    ('toys', 'Toys & Games'),
    ('automotive', 'Automotive & Tools'),
    ('grocery', 'Gourmet & Grocery'),
    ('stationery', 'Office & Stationery'),
    ('gaming', 'Gaming & Consoles'),
]


class Product(models.Model):
    """Model representing a product in the store."""
    name = models.CharField(max_length=255)
    brand = models.CharField(max_length=100, blank=True, default='')
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2, help_text='Price in INR')
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='electronics')
    stock = models.PositiveIntegerField(default=10)
    is_featured = models.BooleanField(default=False)
    discount_percent = models.PositiveIntegerField(default=0, help_text='Discount percentage (0-99)')
    rating = models.DecimalField(max_digits=2, decimal_places=1, default=4.0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Product'
        verbose_name_plural = 'Products'

    def __str__(self):
        return self.name

    @property
    def discounted_price(self):
        """Calculate the price after discount using Decimal arithmetic only."""
        if self.discount_percent > 0:
            discount_factor = Decimal('1') - (Decimal(str(self.discount_percent)) / Decimal('100'))
            return (self.price * discount_factor).quantize(Decimal('0.01'))
        return self.price

    @property
    def discount_amount(self):
        """Calculate the discount savings amount per unit in INR."""
        if self.discount_percent > 0:
            return (self.price - self.discounted_price).quantize(Decimal('0.01'))
        return Decimal('0.00')

    @property
    def in_stock(self):
        return self.stock > 0



class Wishlist(models.Model):
    """Model representing a product saved in a user's wishlist."""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='wishlist_items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='wishlisted_by')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'product')
        ordering = ['-created_at']
        verbose_name = 'Wishlist Item'
        verbose_name_plural = 'Wishlist Items'

    def __str__(self):
        return f"{self.user.username} - {self.product.name}"

