from django.shortcuts import render

from django.http import JsonResponse
from .models import *
import json

# Create your views here.
def cart(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
    else:
        items = []
        order = {'get_cart_total': 0,
                 'get_cart_total_price': 0}
    
    context = {'order': order, 'items': items}
    return render(request, 'base/cart.html', context)

def store(request):
    products = Product.objects.all()
    context = {'products': products}
    return render(request, 'base/store.html', context)

def checkout(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
    else:
        items = []
        order = {'get_cart_total': 0,
                 'get_cart_total_price': 0}
    
    context = {'order': order, 'items': items}
    return render(request, 'base/checkout.html', context)

def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    print('productId', productId, 'action:', action)
    
    customer = request.user.customer
    product = Product.obcjets.get(id=productId)
    return JsonResponse('Item was added', safe=False)