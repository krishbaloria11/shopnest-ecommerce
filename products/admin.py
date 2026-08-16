from django.contrib import admin
from .models import Product, Wishlist


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'brand', 'category', 'price', 'discount_percent', 'stock', 'is_featured', 'rating', 'created_at')
    list_filter = ('category', 'is_featured', 'created_at')
    search_fields = ('name', 'brand', 'description')
    list_editable = ('is_featured', 'stock', 'discount_percent')
    readonly_fields = ('created_at',)
    ordering = ('-created_at',)


@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('user__username', 'product__name')
    readonly_fields = ('created_at',)

