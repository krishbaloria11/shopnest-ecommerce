from decimal import Decimal
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from products.models import Product
from .models import CartItem


@login_required
def cart_view(request):
    """Display the user's cart with all items, list subtotal, discount savings, and payable total."""
    cart_items = CartItem.objects.filter(user=request.user).select_related('product')
    original_total = sum((item.product.price * item.quantity for item in cart_items), Decimal('0.00'))
    total = sum((item.product.discounted_price * item.quantity for item in cart_items), Decimal('0.00'))
    discount_savings = (original_total - total).quantize(Decimal('0.01'))

    return render(request, 'cart/cart.html', {
        'cart_items': cart_items,
        'original_total': original_total,
        'total': total,
        'discount_savings': discount_savings,
    })



@login_required
def add_to_cart(request, product_id):
    """Add a product to the user's cart or increment its quantity. Supports AJAX."""
    product = get_object_or_404(Product, pk=product_id)

    if not product.in_stock:
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'status': 'error', 'message': f'"{product.name}" is out of stock.'})
        messages.error(request, f'"{product.name}" is out of stock.')
        return redirect(request.META.get('HTTP_REFERER', 'products:home'))

    cart_item, created = CartItem.objects.get_or_create(
        user=request.user,
        product=product,
        defaults={'quantity': 1}
    )
    if not created:
        cart_item.quantity += 1
        cart_item.save()
        msg = f'Updated "{product.name}" quantity to {cart_item.quantity}.'
    else:
        msg = f'Added "{product.name}" to your cart.'

    # AJAX response
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        cart_count = CartItem.objects.filter(user=request.user).count()
        return JsonResponse({'status': 'success', 'message': msg, 'cart_count': cart_count})

    messages.success(request, msg)
    next_url = request.POST.get('next', request.META.get('HTTP_REFERER', 'cart:cart_view'))
    return redirect(next_url)


@login_required
def remove_from_cart(request, item_id):
    """Remove an item from the user's cart."""
    cart_item = get_object_or_404(CartItem, pk=item_id, user=request.user)
    product_name = cart_item.product.name
    cart_item.delete()
    messages.success(request, f'Removed "{product_name}" from your cart.')
    return redirect('cart:cart_view')


@login_required
def update_quantity(request, item_id):
    """Update the quantity of a cart item."""
    cart_item = get_object_or_404(CartItem, pk=item_id, user=request.user)
    if request.method == 'POST':
        try:
            quantity = int(request.POST.get('quantity', 1))
            if quantity < 1:
                cart_item.delete()
                messages.success(request, f'Removed "{cart_item.product.name}" from your cart.')
            else:
                cart_item.quantity = quantity
                cart_item.save()
                messages.success(request, f'Updated "{cart_item.product.name}" quantity to {quantity}.')
        except (ValueError, TypeError):
            messages.error(request, 'Invalid quantity.')
    return redirect('cart:cart_view')


@login_required
def increase_quantity(request, item_id):
    """Increase cart item quantity by 1."""
    cart_item = get_object_or_404(CartItem, pk=item_id, user=request.user)
    cart_item.quantity += 1
    cart_item.save()
    return redirect('cart:cart_view')


@login_required
def decrease_quantity(request, item_id):
    """Decrease cart item quantity by 1, remove if 0."""
    cart_item = get_object_or_404(CartItem, pk=item_id, user=request.user)
    if cart_item.quantity <= 1:
        cart_item.delete()
        messages.success(request, f'Removed "{cart_item.product.name}" from your cart.')
    else:
        cart_item.quantity -= 1
        cart_item.save()
    return redirect('cart:cart_view')
