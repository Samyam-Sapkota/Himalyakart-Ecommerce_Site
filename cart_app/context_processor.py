from .models import CartItem,Cart
from django.core.exceptions import ObjectDoesNotExist

def cart_counter(request):
    count = 0
    user =request.user
    if user.is_authenticated:

       
            cart = Cart.objects.filter(user=request.user)
            cart_items = CartItem.objects.all().filter(cart=cart[:1])
            for cart_item in cart_items:
                count += cart_item.quantity

    # except Cart.DoesNotExist:
    # #     count = 0
    return {"cart_count":count}