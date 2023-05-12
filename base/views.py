from django.shortcuts import render, redirect

from django.http import JsonResponse, HttpResponse
from .models import *
from .forms import ShippingForm
from .utils import cookieCart, cartData, deleteCartAndRedirect, guestOrder
import json
import datetime

# Create your views here.
def cart(request):
    order, items = cartData(request)   
    context = {'order': order, 'items': items}
    return render(request, 'base/cart.html', context)

def store(request):
    products = Product.objects.all()
    context = {'products': products}
    return render(request, 'base/store.html', context)

def checkout(request):
    form = ShippingForm()
    order, items = cartData(request)  
        
    context = {'order': order, 'items': items, 'form': form}
    return render(request, 'base/checkout.html', context)

def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    print('productId', productId, 'action:', action)
    
    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    orderItem, creted = OrderItem.objects.get_or_create(order=order, product=product)
    
    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)
    
    orderItem.save()
    
    if orderItem.quantity <= 0:
        orderItem.delete()
               
    return JsonResponse('Item was added', safe=False)

def processOrder(request):
    if request.method == "POST":
        transaction_id = datetime.datetime.now().timestamp()
        
        if request.user.is_authenticated:
            customer = request.user.customer
            order, created = Order.objects.get_or_create(customer=customer, complete=False)
            
        else:
            order, customer = guestOrder(request)
                
        if order.shipping == True:
            ShippingAddress.objects.create(
                customer = customer,
                order = order,
                address = request.POST.get('address'),
                city = request.POST.get('city'),
                state = request.POST.get('state'),
                zipcode = request.POST.get('zipcode'),
            )   
            
        order.transaction_id = transaction_id
        order.complete = True
        order.save()
        return deleteCartAndRedirect(request)
        
    return HttpResponse('not POST request')
    