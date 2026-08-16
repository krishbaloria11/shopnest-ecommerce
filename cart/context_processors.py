from decimal import Decimal
from django.conf import settings
from .models import CartItem
from products.models import Wishlist


def cart_context(request):
    """Context processor providing cart count, total, original total, savings, wishlist count, and currency info to all templates using Decimal."""
    cart_count = 0
    cart_total = Decimal('0.00')
    cart_original_total = Decimal('0.00')
    cart_savings = Decimal('0.00')
    wishlist_count = 0

    if request.user.is_authenticated:
        items = list(CartItem.objects.filter(user=request.user).select_related('product'))
        cart_count = len(items)
        cart_total = sum((item.product.discounted_price * item.quantity for item in items), Decimal('0.00'))
        cart_original_total = sum((item.product.price * item.quantity for item in items), Decimal('0.00'))
        cart_savings = (cart_original_total - cart_total).quantize(Decimal('0.01'))
        try:
            wishlist_count = Wishlist.objects.filter(user=request.user).count()
        except Exception:
            wishlist_count = 0

    # Currency from session
    currency = request.session.get('currency', 'INR')
    rate = getattr(settings, 'CURRENCY_CONVERSION_RATE', 83)
    if currency == 'USD':
        currency_symbol = '$'
        conversion_rate = Decimal('1') / Decimal(str(rate))
    else:
        currency_symbol = '₹'
        conversion_rate = Decimal('1')

    return {
        'cart_count': cart_count,
        'cart_total': cart_total,
        'cart_original_total': cart_original_total,
        'cart_savings': cart_savings,
        'wishlist_count': wishlist_count,
        'currency': currency,
        'currency_symbol': currency_symbol,
        'conversion_rate': conversion_rate,
    }


