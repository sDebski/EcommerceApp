from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse, HttpResponse
from .models import *
from .forms import *
from django.db.models import Q
from .utils import cookieCart, cartData, deleteCartAndRedirect, guestOrder
import json
import datetime

# Create your views here.


def registerView(request):
    user_form = UserForm()
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('store')
        else:
            print(request, 'An error occured during registration in user form.')
        
    context = {
        'user_form': user_form,
    }
    return render(request, 'base/register.html', context)
    
def loginView(request):
    if request.user.is_authenticated:
        return redirect('store')
    
    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')
        
        try:
            user = User.objects.get(username=username)
        except:
            print(request, 'User does not exist')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return deleteCartAndRedirect(request)
        else:
            print(request, 'Email or password does not exist')
    context = {}
    return render(request, 'base/login.html', context)

def logoutView(request):
    logout(request)
    return deleteCartAndRedirect(request)
    
def cart(request):
    order, items = cartData(request)   
    context = {'order': order, 'items': items}
    return render(request, 'base/cart.html', context)

def store(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    products = Product.objects.filter(
        Q(category__name__icontains=q) 
        )
    paginator = Paginator(products, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    categories = Category.objects.all()
    
    context = {'page_obj': page_obj, 'categories': categories}
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
        my_rating = ProductRating.objects.get(product=product, customer = request.user.customer).value
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
               'my_rating': my_rating,
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