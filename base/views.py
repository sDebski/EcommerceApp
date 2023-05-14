from django.shortcuts import render, redirect
from django.core.paginator import Paginator
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

def viewItem(request, pk):
    product = Product.objects.get(id=pk)
    comments = product.comment_set.all().order_by('-date_added')
    paginator = Paginator(comments, 2)
    
    
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    ratings = product.productrating_set.all()
    try:
        my_rating = ProductRating.objects.get(product=product, customer = request.user.customer)
    except:
        print('zez')
        my_rating = 0
    try:
        rating_mean = sum([rating.value for rating in ratings])/len(ratings)
    except:
        rating_mean = 0
    context = {'product': product,
               'rating_mean': rating_mean,
               'comments': comments,
               'rating_amount': len(ratings),
               'my_rating': my_rating.value,
               'page_obj': page_obj}
    return render(request, 'base/view_item.html', context)

def ratingItem(request, pk, value):
    if request.user.is_authenticated:
        try:
            product = Product.objects.get(id=pk)
        except:
            product = None
        print(product, value)
        if product and int(value) in [1,2,3,4,5]:  
            rating, created = ProductRating.objects.get_or_create(customer = request.user.customer, product = product)
            rating.value = value
            rating.save()
            print('udalo sie')
            return redirect('view-item', pk = pk)
        else: 
            return HttpResponse('No product or wrong rating')
    else:
        return redirect('store')
    
    return HttpResponse(str(pk) + ' ' + str(value))
    
def commentItem(request, pk):
    if request.user.is_authenticated:
        if request.method == 'POST':
            product = Product.objects.get(id=pk)
            content = request.POST.get('body')
            Comment.objects.create(
                customer = request.user.customer,
                content = content,
                product = product
            )
            return redirect('view-item', pk=pk)
    else:
        return redirect('store')