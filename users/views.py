from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import OperationalError
from .forms import UserRegisterForm, UserProfileForm
from orders.models import Order


def register_view(request):
    """Handle user registration with auto-login."""
    if request.user.is_authenticated:
        return redirect('products:home')

    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Welcome, {user.username}! Account created successfully.')
            return redirect('products:home')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = UserRegisterForm()

    return render(request, 'users/register.html', {'form': form})


def login_view(request):
    """Handle user login."""
    if request.user.is_authenticated:
        return redirect('products:home')

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {username}! Logged in successfully.')
                next_url = request.GET.get('next', 'products:home')
                return redirect(next_url)
            else:
                messages.error(request, 'Invalid username or password.')
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = AuthenticationForm()

    for field_name, field in form.fields.items():
        field.widget.attrs['class'] = 'form-control'
        field.widget.attrs['placeholder'] = field.label

    return render(request, 'users/login.html', {'form': form})


def logout_view(request):
    """Handle user logout."""
    logout(request)
    messages.info(request, 'Logged out successfully.')
    return redirect('products:home')


@login_required
def profile(request):
    """Display user profile dashboard with order and wishlist stats."""
    from products.models import Wishlist
    try:
        order_count = Order.objects.filter(user=request.user).count()
        recent_orders = Order.objects.filter(user=request.user)[:5]
    except OperationalError:
        order_count = 0
        recent_orders = []

    try:
        wishlist_count = Wishlist.objects.filter(user=request.user).count()
        recent_wishlist = Wishlist.objects.filter(user=request.user).select_related('product')[:4]
    except Exception:
        wishlist_count = 0
        recent_wishlist = []

    return render(request, 'users/profile.html', {
        'order_count': order_count,
        'recent_orders': recent_orders,
        'wishlist_count': wishlist_count,
        'recent_wishlist': recent_wishlist,
    })



# Alias for backward compatibility
profile_view = profile


@login_required
def edit_profile_view(request):
    """Edit user profile details."""
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('users:profile')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = UserProfileForm(instance=request.user)

    return render(request, 'users/edit_profile.html', {'form': form})


def toggle_currency(request):
    """Toggle between INR and USD, storing preference in session."""
    current = request.session.get('currency', 'INR')
    request.session['currency'] = 'USD' if current == 'INR' else 'INR'
    return redirect(request.META.get('HTTP_REFERER', 'products:home'))
