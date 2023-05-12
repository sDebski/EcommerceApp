import json
from django.http import HttpResponseRedirect
from .models import *

def deleteCartAndRedirect(request):
    response = HttpResponseRedirect('/')
    response.delete_cookie('cart')
    return response


def cookieCart(request):
    try:
        cart = json.loads(request.COOKIES['cart'])
    except:
        cart = {}
            
    items = []
    order = {'get_cart_total': 0,
                'get_cart_total_price': 0,
                'shipping': False}

    for i in cart:
        try:
            product = Product.objects.get(id=i)
            total = (product.price * cart[i]['quantity']) 
            
            order['get_cart_total_price'] += total
            order['get_cart_total'] += cart[i]['quantity']
            
            item = {
                'product': {
                    'id': product.id,
                    'name': product.name,
                    'price': product.price,
                    'imageURL': product.imageURL,
                },
                'quantity': cart[i]['quantity'],
                'get_total': total,
            }
            items.append(item)
            
            if product.digital == False:
                order['shipping'] = True
        except:
            pass
        
    return order, items

def cartData(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
    else:
        order, items = cookieCart(request)  
    
    return order, items

def guestOrder(request):
    name = request.POST.get('name')
    email = request.POST.get('email')
    order, items = cookieCart(request)
    
    customer, created = Customer.objects.get_or_create(
        email=email,
        )
    customer.name = name
    customer.save()
    
    order = Order.objects.create(
        customer=customer,
        complete=False,
    )
    
    for item in items:
        try:
            product = Product.objects.get(id=item['product']['id'])
            orderItem = OrderItem.objects.create(
                product=product,
                order=order,
                quantity=item['quantity']
            )
        except:
            pass
        
    return order, customer