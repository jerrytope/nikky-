from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.conf import settings
from cart.models import Cart, CartItem
from .models import Order, OrderItem
from .forms import OrderCreateForm
import requests
import json


@login_required
def order_create(request):
    """Create order from cart"""
    try:
        cart = Cart.objects.get(user=request.user)
        if not cart.items.exists():
            messages.error(request, "Your cart is empty.")
            return redirect("cart:cart_detail")
    except Cart.DoesNotExist:
        messages.error(request, "Your cart is empty.")
        return redirect("cart:cart_detail")

    if request.method == "POST":
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.total_amount = cart.total_price
            order.save()

            # Create order items
            for cart_item in cart.items.all():
                OrderItem.objects.create(
                    order=order,
                    product=cart_item.product,
                    price=cart_item.product.get_price,
                    quantity=cart_item.quantity,
                )

            # Clear cart
            cart.items.all().delete()

            # Redirect to payment
            return redirect("orders:initiate_payment", order_id=order.id)
    else:
        # Pre-fill form with user data
        initial_data = {
            "email": request.user.email,
            "first_name": request.user.first_name,
            "last_name": request.user.last_name,
        }
        form = OrderCreateForm(initial=initial_data)

    return render(request, "orders/order_create.html", {"form": form, "cart": cart})


@login_required
def initiate_payment(request, order_id):
    """Initiate Paystack payment"""
    order = get_object_or_404(Order, id=order_id, user=request.user)

    if order.payment_status == "paid":
        return redirect("orders:order_success", order_id=order.id)

    # Paystack payment initialization
    url = "https://api.paystack.co/transaction/initialize"
    headers = {
        "Authorization": f"Bearer {settings.PAYSTACK_SECRET_KEY}",
        "Content-Type": "application/json",
    }

    data = {
        "email": order.email,
        "amount": int(order.total_amount * 100),  # Convert to kobo
        "reference": str(order.id),
        "callback_url": request.build_absolute_uri(f"/orders/verify-payment/"),
        "metadata": {
            "order_id": str(order.id),
            "customer_name": order.full_name,
        },
    }

    try:
        response = requests.post(url, headers=headers, data=json.dumps(data))
        response_data = response.json()

        if response_data.get("status"):
            authorization_url = response_data["data"]["authorization_url"]
            order.payment_reference = response_data["data"]["reference"]
            order.save()
            return redirect(authorization_url)
        else:
            messages.error(request, "Payment initialization failed. Please try again.")
    except Exception as e:
        messages.error(request, "Payment service unavailable. Please try again later.")

    return redirect("orders:order_detail", order_id=order.id)


@csrf_exempt
def verify_payment(request):
    """Verify Paystack payment"""
    reference = request.GET.get("reference")

    if not reference:
        messages.error(request, "Invalid payment reference.")
        return redirect("products:product_list")

    # Verify payment with Paystack
    url = f"https://api.paystack.co/transaction/verify/{reference}"
    headers = {
        "Authorization": f"Bearer {settings.PAYSTACK_SECRET_KEY}",
    }

    try:
        response = requests.get(url, headers=headers)
        response_data = response.json()

        if response_data.get("status") and response_data["data"]["status"] == "success":
            order_id = response_data["data"]["metadata"]["order_id"]
            order = get_object_or_404(Order, id=order_id)

            if order.payment_status != "paid":
                order.payment_status = "paid"
                order.status = "processing"
                order.save()

                # Update product stock
                for item in order.items.all():
                    product = item.product
                    product.stock -= item.quantity
                    product.save()

            return redirect("orders:order_success", order_id=order.id)
        else:
            messages.error(request, "Payment verification failed.")
    except Exception as e:
        messages.error(request, "Payment verification error.")

    return redirect("products:product_list")


@login_required
def order_success(request, order_id):
    """Order success page"""
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, "orders/order_success.html", {"order": order})


@login_required
def order_list(request):
    """List user's orders"""
    orders = Order.objects.filter(user=request.user)
    return render(request, "orders/order_list.html", {"orders": orders})


@login_required
def order_detail(request, order_id):
    """Order detail page"""
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, "orders/order_detail.html", {"order": order})
