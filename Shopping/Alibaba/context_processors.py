from .models import CartItem,Cart

def get_items_count(request):
    cart_count = 0

    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user, is_ordered=False).first()
        if cart:
            cart_count = CartItem.objects.filter(cart=cart).count()
    
    return {'cart_count': cart_count}