from .models import Cart


def cart(request):
    """Add cart information to template context"""
    cart_total_items = 0
    cart_total_price = 0
    
    if request.user.is_authenticated:
        try:
            cart_obj = Cart.objects.get(user=request.user)
            cart_total_items = cart_obj.total_items
            cart_total_price = cart_obj.total_price
        except Cart.DoesNotExist:
            pass
    else:
        # For anonymous users, use session-based cart
        if request.session.session_key:
            try:
                cart_obj = Cart.objects.get(session_key=request.session.session_key)
                cart_total_items = cart_obj.total_items
                cart_total_price = cart_obj.total_price
            except Cart.DoesNotExist:
                pass
    
    return {
        'cart_total_items': cart_total_items,
        'cart_total_price': cart_total_price,
    }
