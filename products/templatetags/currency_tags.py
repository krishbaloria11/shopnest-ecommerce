from decimal import Decimal, InvalidOperation
from django import template
from django.conf import settings

register = template.Library()


@register.simple_tag(takes_context=True)
def format_price(context, value):
    """
    Format price according to session currency setting using pure Decimal arithmetic.
    Base price is in INR (₹).
    If currency is USD, convert using Decimal(1) / Decimal(rate) and format as $XX.XX.
    If currency is INR, format as ₹XX.XX.
    """
    if value is None:
        return ""

    try:
        val = Decimal(str(value))
    except (ValueError, TypeError, InvalidOperation):
        return str(value)

    currency = context.get('currency', 'INR')
    rate = getattr(settings, 'CURRENCY_CONVERSION_RATE', 83)

    try:
        rate_dec = Decimal(str(rate))
    except (ValueError, TypeError, InvalidOperation):
        rate_dec = Decimal('83')

    if currency == 'USD':
        usd_val = val / rate_dec
        return f"${usd_val:,.2f}"
    else:
        return f"₹{val:,.2f}"

