from .models import CartItem

def get_items_count(request):
    cart_count = 0
    if request.user.is_authenticated:
        cart_count = CartItem.objects.filter(user = request.user).count()
        return {'cart_count':cart_count}
    return {'cart_count':cart_count}