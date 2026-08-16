from decimal import Decimal
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.db import models
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from .models import Product, Wishlist, CATEGORY_CHOICES


def home(request):
    """
    Display homepage with hero banner, category explorer, deals/trending,
    rich sorting and filtering (price, category, rating), and pagination.
    """
    all_products = Product.objects.all()

    # Category counts for category pills
    category_counts = {}
    for cat_code, _ in CATEGORY_CHOICES:
        category_counts[cat_code] = Product.objects.filter(category=cat_code).count()

    # Category filter
    category = request.GET.get('category', '').strip()
    if category:
        all_products = all_products.filter(category=category)

    # Brand filter
    brand = request.GET.get('brand', '').strip()
    if brand:
        all_products = all_products.filter(brand__iexact=brand)

    # Price range filter
    min_price = request.GET.get('min_price', '').strip()
    max_price = request.GET.get('max_price', '').strip()
    if min_price:
        try:
            all_products = all_products.filter(price__gte=Decimal(min_price))
        except (ValueError, TypeError):
            pass
    if max_price:
        try:
            all_products = all_products.filter(price__lte=Decimal(max_price))
        except (ValueError, TypeError):
            pass

    # In-stock filter
    in_stock_only = request.GET.get('in_stock', '')
    if in_stock_only == '1':
        all_products = all_products.filter(stock__gt=0)

    # Sorting
    sort = request.GET.get('sort', 'featured')
    if sort == 'price_low':
        all_products = all_products.order_by('price')
    elif sort == 'price_high':
        all_products = all_products.order_by('-price')
    elif sort == 'rating':
        all_products = all_products.order_by('-rating', '-created_at')
    elif sort == 'discount':
        all_products = all_products.order_by('-discount_percent', '-created_at')
    elif sort == 'newest':
        all_products = all_products.order_by('-created_at')
    else:  # featured or default
        all_products = all_products.order_by('-is_featured', '-rating', '-created_at')

    # Top deals / Flash sale for homepage section (discounts >= 15%)
    flash_deals = Product.objects.filter(discount_percent__gte=15).order_by('-discount_percent')[:6]

    # Featured products for trending showcase
    featured_products = Product.objects.filter(is_featured=True)[:8]

    # User's wishlist set for active heart icons
    user_wishlist_ids = set()
    if request.user.is_authenticated:
        user_wishlist_ids = set(
            Wishlist.objects.filter(user=request.user).values_list('product_id', flat=True)
        )

    # Pagination (12 items per page)
    paginator = Paginator(all_products, 12)
    page_number = request.GET.get('page')
    products_page = paginator.get_page(page_number)

    return render(request, 'products/home.html', {
        'featured_products': featured_products,
        'flash_deals': flash_deals,
        'products': products_page,
        'categories': CATEGORY_CHOICES,
        'category_counts': category_counts,
        'current_category': category,
        'current_brand': brand,
        'current_sort': sort,
        'min_price': min_price,
        'max_price': max_price,
        'in_stock_only': in_stock_only,
        'user_wishlist_ids': user_wishlist_ids,
        'total_catalog_count': Product.objects.count(),
    })


def product_detail(request, pk):
    """Display comprehensive details for a single product."""
    product = get_object_or_404(Product, pk=pk)
    related_products = Product.objects.filter(category=product.category).exclude(pk=pk)[:4]

    is_wishlisted = False
    user_wishlist_ids = set()
    if request.user.is_authenticated:
        is_wishlisted = Wishlist.objects.filter(user=request.user, product=product).exists()
        user_wishlist_ids = set(
            Wishlist.objects.filter(user=request.user).values_list('product_id', flat=True)
        )

    return render(request, 'products/product_detail.html', {
        'product': product,
        'related_products': related_products,
        'is_wishlisted': is_wishlisted,
        'user_wishlist_ids': user_wishlist_ids,
    })


def search(request):
    """Search products by name, brand, or description with sorting."""
    query = request.GET.get('q', '').strip()
    category = request.GET.get('category', '').strip()
    sort = request.GET.get('sort', 'relevance')

    results = Product.objects.all()

    if query:
        results = results.filter(
            models.Q(name__icontains=query) |
            models.Q(description__icontains=query) |
            models.Q(brand__icontains=query) |
            models.Q(category__icontains=query)
        )
    elif not category:
        results = Product.objects.none()

    if category:
        results = results.filter(category=category)

    # Sorting
    if sort == 'price_low':
        results = results.order_by('price')
    elif sort == 'price_high':
        results = results.order_by('-price')
    elif sort == 'rating':
        results = results.order_by('-rating')
    elif sort == 'newest':
        results = results.order_by('-created_at')
    elif sort == 'discount':
        results = results.order_by('-discount_percent')
    else:
        results = results.order_by('-is_featured', '-rating')

    user_wishlist_ids = set()
    if request.user.is_authenticated:
        user_wishlist_ids = set(
            Wishlist.objects.filter(user=request.user).values_list('product_id', flat=True)
        )

    paginator = Paginator(results, 12)
    page_number = request.GET.get('page')
    products_page = paginator.get_page(page_number)

    return render(request, 'products/search.html', {
        'query': query,
        'products': products_page,
        'current_category': category,
        'current_sort': sort,
        'categories': CATEGORY_CHOICES,
        'user_wishlist_ids': user_wishlist_ids,
    })


@login_required
def toggle_wishlist(request, pk):
    """Add or remove a product from the user's wishlist. Supports AJAX."""
    product = get_object_or_404(Product, pk=pk)
    wishlist_item = Wishlist.objects.filter(user=request.user, product=product).first()

    if wishlist_item:
        wishlist_item.delete()
        action = 'removed'
        msg = f'Removed "{product.name}" from your Wishlist.'
    else:
        Wishlist.objects.create(user=request.user, product=product)
        action = 'added'
        msg = f'Added "{product.name}" to your Wishlist.'

    wishlist_count = Wishlist.objects.filter(user=request.user).count()

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest' or request.GET.get('format') == 'json':
        return JsonResponse({
            'status': 'success',
            'action': action,
            'message': msg,
            'wishlist_count': wishlist_count,
            'product_id': product.pk,
        })

    messages.success(request, msg)
    return redirect(request.META.get('HTTP_REFERER', 'products:home'))


@login_required
def wishlist_view(request):
    """Display all products saved in the user's wishlist."""
    wishlist_items = Wishlist.objects.filter(user=request.user).select_related('product')
    products = [item.product for item in wishlist_items]

    user_wishlist_ids = {p.id for p in products}

    return render(request, 'products/wishlist.html', {
        'wishlist_items': wishlist_items,
        'products': products,
        'user_wishlist_ids': user_wishlist_ids,
        'wishlist_count': len(products),
    })
