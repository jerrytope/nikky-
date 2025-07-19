from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from products.models import Product
from .models import Cart, CartItem
from .cart import CartSession


def get_or_create_cart(request):
    """Get or create cart for authenticated user or session"""
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
        return cart
    else:
        # For anonymous users, use session-based cart
        if not request.session.session_key:
            request.session.create()
        cart, created = Cart.objects.get_or_create(
            session_key=request.session.session_key
        )
        return cart


def cart_detail(request):
    """Display cart contents"""
    cart = get_or_create_cart(request)
    return render(request, "cart/cart_detail.html", {"cart": cart})


@require_POST
def cart_add(request, product_id):
    """Add product to cart"""
    product = get_object_or_404(Product, id=product_id, available=True)
    cart = get_or_create_cart(request)
    quantity = int(request.POST.get("quantity", 1))

    # Check stock availability
    if quantity > product.stock:
        messages.error(request, f"Only {product.stock} items available in stock.")
        return redirect("products:product_detail", slug=product.slug)

    cart_item, created = CartItem.objects.get_or_create(
        cart=cart, product=product, defaults={"quantity": quantity}
    )

    if not created:
        # Update quantity if item already exists
        new_quantity = cart_item.quantity + quantity
        if new_quantity > product.stock:
            messages.error(
                request, f"Cannot add more items. Only {product.stock} available."
            )
            return redirect("products:product_detail", slug=product.slug)
        cart_item.quantity = new_quantity
        cart_item.save()

    messages.success(request, f"{product.name} added to cart.")

    if request.headers.get("X-Requested-With") == "XMLHttpRequest":
        return JsonResponse(
            {
                "success": True,
                "cart_total_items": cart.total_items,
                "cart_total_price": float(cart.total_price),
            }
        )

    return redirect("cart:cart_detail")


@require_POST
def cart_remove(request, product_id):
    """Remove product from cart"""
    product = get_object_or_404(Product, id=product_id)
    cart = get_or_create_cart(request)

    try:
        cart_item = CartItem.objects.get(cart=cart, product=product)
        cart_item.delete()
        messages.success(request, f"{product.name} removed from cart.")
    except CartItem.DoesNotExist:
        messages.error(request, "Item not found in cart.")

    return redirect("cart:cart_detail")


@require_POST
def cart_update(request, product_id):
    """Update product quantity in cart"""
    product = get_object_or_404(Product, id=product_id)
    cart = get_or_create_cart(request)
    quantity = int(request.POST.get("quantity", 1))

    if quantity > product.stock:
        messages.error(request, f"Only {product.stock} items available.")
        return redirect("cart:cart_detail")

    try:
        cart_item = CartItem.objects.get(cart=cart, product=product)
        if quantity > 0:
            cart_item.quantity = quantity
            cart_item.save()
            messages.success(request, "Cart updated successfully.")
        else:
            cart_item.delete()
            messages.success(request, f"{product.name} removed from cart.")
    except CartItem.DoesNotExist:
        messages.error(request, "Item not found in cart.")

    return redirect("cart:cart_detail")


def cart_clear(request):
    """Clear all items from cart"""
    cart = get_or_create_cart(request)
    cart.items.all().delete()
    messages.success(request, "Cart cleared successfully.")
    return redirect("cart:cart_detail")
