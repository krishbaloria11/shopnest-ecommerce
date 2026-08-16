from django.db import models
from django.contrib.auth.models import User
from products.models import Product


class CartItem(models.Model):
    """Model representing an item in a user's cart."""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cart_items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-added_at']
        unique_together = ('user', 'product')
        verbose_name = 'Cart Item'
        verbose_name_plural = 'Cart Items'

    def __str__(self):
        return f"{self.quantity}x {self.product.name} ({self.user.username})"

    @property
    def subtotal(self):
        """Calculate the payable subtotal for this cart item (after discount)."""
        return self.product.discounted_price * self.quantity

    @property
    def original_subtotal(self):
        """Calculate the original list subtotal for this cart item (before discount)."""
        return self.product.price * self.quantity

    @property
    def discount_savings(self):
        """Calculate the total savings amount for this cart item."""
        return (self.original_subtotal - self.subtotal).quantize(self.product.price)

