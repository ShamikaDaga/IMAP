from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from .models import Product, Category, Wishlist, Order, OrderItem
from .forms import SignUpForm, CheckoutForm
import random
import string

def generate_order_number():
    return ''.join(random.choices(string.digits, k=6))

def home(request):
    """Homepage view"""
    categories = Category.objects.all()
    featured_products = Product.objects.filter(is_active=True)[:6]
    return render(request, 'desserts/index.html', {
        'categories': categories,
        'featured_products': featured_products
    })

def pies_list(request):
    """Pies listing page"""
    category = get_object_or_404(Category, slug='pies')
    products = Product.objects.filter(category=category, is_active=True)
    return render(request, 'desserts/piespage.html', {
        'category': category,
        'products': products
    })

def cupcakes_list(request):
    """Cupcakes listing page"""
    category = get_object_or_404(Category, slug='cupcakes')
    products = Product.objects.filter(category=category, is_active=True)
    return render(request, 'desserts/cupcakespage.html', {
        'category': category,
        'products': products
    })

def product_detail(request, slug):
    """Product detail page"""
    product = get_object_or_404(Product, slug=slug, is_active=True)
    return render(request, 'desserts/productpage.html', {
        'product': product
    })

@login_required
def wishlist(request):
    """User wishlist page"""
    wishlist_items = Wishlist.objects.filter(user=request.user).select_related('product')
    return render(request, 'desserts/wishlist.html', {
        'wishlist_items': wishlist_items
    })

@login_required
def add_to_wishlist(request, product_id):
    """Add product to wishlist"""
    product = get_object_or_404(Product, id=product_id)
    Wishlist.objects.get_or_create(user=request.user, product=product)
    messages.success(request, f'{product.name} added to wishlist!')
    return redirect(request.META.get('HTTP_REFERER', 'home'))

@login_required
def remove_from_wishlist(request, item_id):
    """Remove product from wishlist"""
    item = get_object_or_404(Wishlist, id=item_id, user=request.user)
    item.delete()
    messages.success(request, 'Item removed from wishlist!')
    return redirect('wishlist')

def payment(request):
    """Payment page"""
    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            # Create order
            order = Order.objects.create(
                user=request.user if request.user.is_authenticated else None,
                order_number=generate_order_number(),
                total_amount=0,  # Calculate from cart
                customer_name=form.cleaned_data['name'],
                customer_email=form.cleaned_data['email'],
                customer_address=form.cleaned_data['address']
            )
            # Add items from cart session
            # Process payment
            return redirect('receipt', order_id=order.id)
    else:
        form = CheckoutForm()

    return render(request, 'desserts/payment.html', {
        'form': form
    })

def receipt(request, order_id):
    """Order receipt page"""
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'desserts/Receipt_page.html', {
        'order': order
    })

def signin(request):
    """User sign in page"""
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {username}!')
                return redirect('home')
    else:
        form = AuthenticationForm()

    return render(request, 'desserts/signin.html', {
        'form': form
    })

def signup(request):
    """User registration page"""
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Account created successfully!')
            return redirect('home')
    else:
        form = SignUpForm()

    return render(request, 'desserts/signup.html', {
        'form': form
    })

def signout(request):
    """User logout"""
    logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('home')
