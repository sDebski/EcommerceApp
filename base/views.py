from django.shortcuts import render
from .models import *
# Create your views here.
def cart(request):
    context = {}
    return render(request, 'base/cart.html', context)

def store(request):
    products = Product.objects.all()
    context = {'products': products}
    return render(request, 'base/store.html', context)

def checkout(request):
    context = {}
    return render(request, 'base/checkout.html', context)