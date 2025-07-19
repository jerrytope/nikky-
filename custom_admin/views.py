from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.contrib.auth.models import User
from django.db.models import Count, Sum
from django.utils import timezone
from datetime import datetime, timedelta
from products.models import Product
from orders.models import Order
from cart.models import Cart, CartItem
from .forms import ProductForm, CategoryForm


def is_admin(user):
    """Check if user is admin"""
    return user.is_authenticated and user.is_staff


@login_required
@user_passes_test(is_admin)
def admin_dashboard(request):
    """Custom admin dashboard"""
    # Get statistics
    total_products = Product.objects.count()
    total_orders = Order.objects.count()
    total_users = User.objects.count()
    
    # Recent orders
    recent_orders = Order.objects.select_related('user').order_by('-created_at')[:5]
    
    # Recent products
    recent_products = Product.objects.order_by('-created_at')[:5]
    
    # Sales statistics (last 7 days)
    seven_days_ago = timezone.now() - timedelta(days=7)
    recent_sales = Order.objects.filter(
        created_at__gte=seven_days_ago,
        status='completed'
    ).aggregate(total_sales=Sum('total_amount'))['total_sales'] or 0
    
    context = {
        'total_products': total_products,
        'total_orders': total_orders,
        'total_users': total_users,
        'recent_sales': recent_sales,
        'recent_orders': recent_orders,
        'recent_products': recent_products,
    }
    
    return render(request, 'custom_admin/dashboard.html', context)


@login_required
@user_passes_test(is_admin)
def admin_products(request):
    """Manage products"""
    products = Product.objects.select_related('category').all().order_by('-created_at')
    
    if request.method == 'POST':
        action = request.POST.get('action')
        product_id = request.POST.get('product_id')
        
        if action == 'delete' and product_id:
            product = get_object_or_404(Product, id=product_id)
            product.delete()
            messages.success(request, f'Product "{product.name}" deleted successfully.')
            return redirect('custom_admin:products')
    
    context = {
        'products': products,
    }
    return render(request, 'custom_admin/products.html', context)


@login_required
@user_passes_test(is_admin)
def add_product(request):
    """Add new product"""
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            # Save the main product
            product = form.save(commit=False)
            
            # Handle discount price
            if form.cleaned_data.get('discount_price'):
                product.discount_price = form.cleaned_data['discount_price']
            
            product.save()
            
            messages.success(request, f'Product "{product.name}" added successfully.')
            return redirect('custom_admin:products')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = ProductForm()
    
    context = {
        'form': form,
        'action': 'Add',
    }
    return render(request, 'custom_admin/product_form.html', context)


@login_required
@user_passes_test(is_admin)
def edit_product(request, product_id):
    """Edit existing product"""
    product = get_object_or_404(Product, id=product_id)
    
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            # Save the main product
            product = form.save(commit=False)
            
            # Handle discount price
            if form.cleaned_data.get('discount_price'):
                product.discount_price = form.cleaned_data['discount_price']
            else:
                product.discount_price = None
            
            product.save()
            
            messages.success(request, f'Product "{product.name}" updated successfully.')
            return redirect('custom_admin:products')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        # Initialize form with current values
        form = ProductForm(instance=product)
        if product.discount_price:
            form.fields['discount_price'].initial = product.discount_price
    
    context = {
        'form': form,
        'product': product,
        'action': 'Edit',
    }
    return render(request, 'custom_admin/product_form.html', context)


@login_required
@user_passes_test(is_admin)
def view_product(request, product_id):
    """View product details"""
    product = get_object_or_404(Product, id=product_id)
    
    context = {
        'product': product,
    }
    return render(request, 'custom_admin/product_detail.html', context)


@login_required
@user_passes_test(is_admin)
def admin_categories(request):
    """Manage categories"""
    from products.models import Category
    categories = Category.objects.all().order_by('name')
    
    if request.method == 'POST':
        action = request.POST.get('action')
        category_id = request.POST.get('category_id')
        
        if action == 'delete' and category_id:
            category = get_object_or_404(Category, id=category_id)
            # Check if category has products
            if category.products.exists():
                messages.error(request, f'Cannot delete category "{category.name}" because it has products.')
            else:
                category.delete()
                messages.success(request, f'Category "{category.name}" deleted successfully.')
            return redirect('custom_admin:categories')
    
    context = {
        'categories': categories,
    }
    return render(request, 'custom_admin/categories.html', context)


@login_required
@user_passes_test(is_admin)
def add_category(request):
    """Add new category"""
    if request.method == 'POST':
        form = CategoryForm(request.POST, request.FILES)
        if form.is_valid():
            from products.models import Category
            category = Category.objects.create(
                name=form.cleaned_data['name'],
                description=form.cleaned_data['description']
            )
            messages.success(request, f'Category "{category.name}" added successfully.')
            return redirect('custom_admin:categories')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = CategoryForm()
    
    context = {
        'form': form,
        'action': 'Add',
    }
    return render(request, 'custom_admin/category_form.html', context)


@login_required
@user_passes_test(is_admin)
def edit_category(request, category_id):
    """Edit existing category"""
    from products.models import Category
    category = get_object_or_404(Category, id=category_id)
    
    if request.method == 'POST':
        form = CategoryForm(request.POST, request.FILES, instance=category)
        if form.is_valid():
            category.name = form.cleaned_data['name']
            category.description = form.cleaned_data['description']
            category.save()
            messages.success(request, f'Category "{category.name}" updated successfully.')
            return redirect('custom_admin:categories')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = CategoryForm(initial={
            'name': category.name,
            'description': category.description
        })
    
    context = {
        'form': form,
        'category': category,
        'action': 'Edit',
    }
    return render(request, 'custom_admin/category_form.html', context)


@login_required
@user_passes_test(is_admin)
def admin_orders(request):
    """Manage orders"""
    orders = Order.objects.select_related('user').all().order_by('-created_at')
    
    if request.method == 'POST':
        action = request.POST.get('action')
        order_id = request.POST.get('order_id')
        new_status = request.POST.get('status')
        
        if action == 'update_status' and order_id and new_status:
            order = get_object_or_404(Order, id=order_id)
            order.status = new_status
            order.save()
            messages.success(request, f'Order #{order.id} status updated to {new_status}.')
            return redirect('custom_admin:orders')
    
    context = {
        'orders': orders,
    }
    return render(request, 'custom_admin/orders.html', context)


@login_required
@user_passes_test(is_admin)
def admin_users(request):
    """Manage users"""
    users = User.objects.all().order_by('-date_joined')
    
    if request.method == 'POST':
        action = request.POST.get('action')
        user_id = request.POST.get('user_id')
        
        if action == 'delete' and user_id:
            user = get_object_or_404(User, id=user_id)
            if user != request.user:  # Prevent self-deletion
                user.delete()
                messages.success(request, f'User "{user.username}" deleted successfully.')
                return redirect('custom_admin:users')
            else:
                messages.error(request, 'You cannot delete your own account.')
    
    context = {
        'users': users,
    }
    return render(request, 'custom_admin/users.html', context)


@login_required
@user_passes_test(is_admin)
def admin_login(request):
    """Custom admin login"""
    if request.user.is_authenticated and request.user.is_staff:
        return redirect('custom_admin:dashboard')
    
    if request.method == 'POST':
        from django.contrib.auth import authenticate, login
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(username=username, password=password)
        if user is not None and user.is_staff:
            login(request, user)
            messages.success(request, f'Welcome back, {user.username}!')
            return redirect('custom_admin:dashboard')
        else:
            messages.error(request, 'Invalid credentials or insufficient permissions.')
    
    return render(request, 'custom_admin/login.html') 