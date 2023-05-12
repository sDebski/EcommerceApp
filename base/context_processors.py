from .models import Order
import json

def cart_items_total(request):
    if request.user.is_authenticated:
        try: 
            customer = request.user.customer
        except: 
            return {'total': 0}
        if customer:
            try:
                order = Order.objects.get(customer=customer, complete=False)
            except:
                return {'total': 0}
            else: 
                return {'total': order.get_cart_total}         
    else:
        try:
            cart = json.loads(request.COOKIES['cart'])
        except:
            cart = {}
        cartItems = 0
        for i in cart:
            cartItems += cart[i]['quantity']
        print('Cart:', cart)
        return {'total': cartItems}
            
    