import uuid
from decimal import Decimal
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import OperationalError, transaction
from django.http import JsonResponse
from cart.models import CartItem
from .models import Order, OrderItem
from .forms import CheckoutForm


@login_required
def checkout_view(request):
    """Display checkout form with full transparent price breakdown and process order placement."""
    cart_items = CartItem.objects.filter(user=request.user).select_related('product')
    if not cart_items.exists():
        messages.warning(request, 'Your cart is empty. Please add items to proceed with checkout.')
        return redirect('products:home')

    # Decimal-safe pricing calculations
    original_total = sum((item.product.price * item.quantity for item in cart_items), Decimal('0.00'))
    total_payable = sum((item.product.discounted_price * item.quantity for item in cart_items), Decimal('0.00'))
    discount_savings = (original_total - total_payable).quantize(Decimal('0.01'))

    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            try:
                with transaction.atomic():
                    # Generate a unique demo transaction/reference ID
                    demo_txn_id = f"SN-{uuid.uuid4().hex[:8].upper()}"
                    payment_method = form.cleaned_data.get('payment_method') or 'card'

                    # Create the order
                    order = Order.objects.create(
                        user=request.user,
                        full_name=form.cleaned_data['full_name'],
                        email=form.cleaned_data['email'],
                        phone=form.cleaned_data['phone'],
                        address=form.cleaned_data['address'],
                        city=form.cleaned_data['city'],
                        state=form.cleaned_data['state'],
                        zip_code=form.cleaned_data['zip_code'],
                        total_amount=total_payable,
                        original_amount=original_total,
                        discount_savings=discount_savings,
                        status='confirmed',
                        payment_method=payment_method,
                        payment_status='paid',
                        transaction_id=demo_txn_id,
                    )

                    # Create order items with original and discounted price snapshots
                    for item in cart_items:
                        OrderItem.objects.create(
                            order=order,
                            product=item.product,
                            product_name=item.product.name,
                            quantity=item.quantity,
                            price_at_purchase=item.product.discounted_price,
                            original_price=item.product.price,
                            discount_percent=item.product.discount_percent,
                        )
                        # Safely deduct stock
                        if item.product.stock >= item.quantity:
                            item.product.stock -= item.quantity
                        else:
                            item.product.stock = 0
                        item.product.save(update_fields=['stock'])

                    # Clear the cart
                    cart_items.delete()

                messages.success(request, f'🎉 Order #{order.pk} placed successfully! Thank you for shopping with ShopNest Pro.')
                return redirect('orders:confirmation', order_id=order.pk)
            except OperationalError:
                messages.error(request, 'Database error occurred. Please ensure all migrations are applied.')
            except Exception as e:
                messages.error(request, f'An error occurred while placing your order: {str(e)}')
        else:
            messages.error(request, 'Please correct the highlighted errors in the form.')
    else:
        # Pre-fill form with user info
        initial_name = f"{request.user.first_name} {request.user.last_name}".strip() or request.user.username
        form = CheckoutForm(initial={
            'full_name': initial_name,
            'email': request.user.email,
            'payment_method': 'card',
        })

    return render(request, 'orders/checkout.html', {
        'form': form,
        'cart_items': cart_items,
        'original_total': original_total,
        'total': total_payable,
        'discount_savings': discount_savings,
    })


@login_required
def cancel_order(request, order_id):
    """
    Cancel an eligible order (status: pending, confirmed, processing).
    Restores product inventory safely and updates payment status.
    Supports both POST/GET standard requests and AJAX.
    """
    order = get_object_or_404(Order, pk=order_id, user=request.user)

    if request.method in ['POST', 'GET']:
        success, msg = order.cancel_order()
        if success:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'status': 'success', 'message': msg, 'order_status': 'cancelled'})
            messages.success(request, f'✅ {msg}')
        else:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'status': 'error', 'message': msg})
            messages.error(request, f'⚠️ {msg}')

    next_url = request.POST.get('next', request.META.get('HTTP_REFERER', 'orders:my_orders'))
    return redirect(next_url)


@login_required
def order_confirmation(request, order_id):
    """Display order confirmation after successful placement with demo payment details."""
    order = get_object_or_404(Order, pk=order_id, user=request.user)
    return render(request, 'orders/confirmation.html', {'order': order})


@login_required
def my_orders(request):
    """Display list of all user orders with cancellation modal triggers."""
    try:
        orders = Order.objects.filter(user=request.user).prefetch_related('items')
    except OperationalError:
        orders = []
        messages.warning(request, 'Order database table not found.')
    return render(request, 'orders/history.html', {'orders': orders})


# Alias for backward compatibility
order_history = my_orders


@login_required
def order_detail(request, order_id):
    """Display comprehensive details and timeline for a single order."""
    order = get_object_or_404(Order, pk=order_id, user=request.user)
    
    # Define timeline progression states
    timeline_steps = [
        {'code': 'pending', 'label': 'Order Placed', 'icon': 'bi-cart-check'},
        {'code': 'confirmed', 'label': 'Confirmed', 'icon': 'bi-patch-check'},
        {'code': 'processing', 'label': 'Processing & Packing', 'icon': 'bi-box-seam'},
        {'code': 'shipped', 'label': 'Shipped', 'icon': 'bi-truck'},
        {'code': 'out_for_delivery', 'label': 'Out for Delivery', 'icon': 'bi-geo-alt'},
        {'code': 'delivered', 'label': 'Delivered', 'icon': 'bi-house-check'},
    ]
    
    # Calculate step index
    status_order = ['pending', 'confirmed', 'processing', 'shipped', 'out_for_delivery', 'delivered']
    current_index = -1
    if order.status in status_order:
        current_index = status_order.index(order.status)

    return render(request, 'orders/detail.html', {
        'order': order,
        'timeline_steps': timeline_steps,
        'current_index': current_index,
    })
