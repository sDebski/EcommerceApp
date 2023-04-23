from .models import Order

def cart_items_total(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        
        order = Order.objects.get(customer=customer, complete=False)
        
        if order:
            return {'total': order.get_cart_total}
        else: 
            return {'total': 0}
    else:
        return {'total': 0}
            
    