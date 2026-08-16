from django.contrib import admin
from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('product', 'product_name', 'quantity', 'original_price', 'price_at_purchase', 'discount_percent', 'subtotal')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'full_name', 'total_amount', 'discount_savings', 'status', 'payment_status', 'payment_method', 'created_at')
    list_filter = ('status', 'payment_status', 'payment_method', 'created_at')
    search_fields = ('full_name', 'email', 'user__username', 'transaction_id')
    list_editable = ('status', 'payment_status')
    readonly_fields = ('created_at', 'updated_at', 'transaction_id')
    inlines = [OrderItemInline]
    ordering = ('-created_at',)

