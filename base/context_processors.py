from .models import Order

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
        return {'total': 0}
            
    