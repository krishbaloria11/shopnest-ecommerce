from decimal import Decimal
from django.db import models
from django.contrib.auth.models import User
from products.models import Product


STATUS_CHOICES = [
    ('pending', 'Pending'),
    ('confirmed', 'Confirmed'),
    ('processing', 'Processing'),
    ('shipped', 'Shipped'),
    ('out_for_delivery', 'Out for Delivery'),
    ('delivered', 'Delivered'),
    ('cancelled', 'Cancelled'),
    ('return_requested', 'Return Requested'),
    ('returned', 'Returned'),
    ('refunded', 'Refunded'),
]

PAYMENT_STATUS_CHOICES = [
    ('paid', 'Paid (Demo Simulation)'),
    ('pending', 'Payment Pending'),
    ('cancelled', 'Cancelled / Void'),
    ('refunded', 'Refunded (Demo Simulation)'),
]

PAYMENT_METHOD_CHOICES = [
    ('card', 'Credit / Debit Card (Demo)'),
    ('upi', 'Instant UPI / QR (Demo)'),
    ('netbanking', 'Net Banking (Demo)'),
    ('cod', 'Cash on Delivery (Demo)'),
]


class Order(models.Model):
    """Model representing a customer order with complete lifecycle & demo payment tracking."""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    full_name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    address = models.TextField()
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=20)
    
    total_amount = models.DecimalField(max_digits=12, decimal_places=2, help_text='Final payable amount after discounts')
    original_amount = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'), help_text='Total before discount')
    discount_savings = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'), help_text='Total saved by customer')
    
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='pending')
    payment_method = models.CharField(max_length=30, choices=PAYMENT_METHOD_CHOICES, default='card')
    payment_status = models.CharField(max_length=30, choices=PAYMENT_STATUS_CHOICES, default='paid')
    transaction_id = models.CharField(max_length=100, blank=True, default='')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'

    def __str__(self):
        return f"Order #{self.pk} by {self.user.username} ({self.get_status_display()})"

    @property
    def item_count(self):
        return self.items.count()

    @property
    def can_be_cancelled(self):
        """Returns True if the order is in an early, cancellable stage."""
        return self.status in ['pending', 'confirmed', 'processing']

    def cancel_order(self):
        """
        Safely cancel an order:
        - Checks eligibility
        - Restores stock inventory for all items
        - Updates order status to cancelled
        - Updates payment status to cancelled
        """
        if not self.can_be_cancelled:
            return False, "This order cannot be cancelled in its current status."

        # Restore product stock inventory
        for item in self.items.select_related('product'):
            if item.product:
                item.product.stock += item.quantity
                item.product.save(update_fields=['stock'])

        self.status = 'cancelled'
        self.payment_status = 'cancelled'
        self.save(update_fields=['status', 'payment_status', 'updated_at'])
        return True, f"Order #{self.pk} has been cancelled successfully. Any demo authorization has been released."


class OrderItem(models.Model):
    """Model representing an individual item within an order with price breakdown."""
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True)
    product_name = models.CharField(max_length=255)
    quantity = models.PositiveIntegerField(default=1)
    
    price_at_purchase = models.DecimalField(max_digits=10, decimal_places=2, help_text='Sale price paid per unit')
    original_price = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'), help_text='Original list price per unit')
    discount_percent = models.PositiveIntegerField(default=0, help_text='Discount percent at purchase')

    class Meta:
        verbose_name = 'Order Item'
        verbose_name_plural = 'Order Items'

    def __str__(self):
        return f"{self.quantity}x {self.product_name}"

    @property
    def subtotal(self):
        """Payable subtotal for this item."""
        return self.price_at_purchase * self.quantity

    @property
    def original_subtotal(self):
        """Original list subtotal before discount."""
        unit_orig = self.original_price if self.original_price > 0 else self.price_at_purchase
        return unit_orig * self.quantity

    @property
    def discount_savings(self):
        """Savings on this item."""
        return max(Decimal('0.00'), self.original_subtotal - self.subtotal)
