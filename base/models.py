from django.db import models
from django.contrib.auth.models import User
import functools
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.

class Customer(models.Model):
    user=models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    name=models.CharField(max_length=250, null=True)
    email=models.EmailField(max_length=250, null=True)
    
    def __str__(self):
        
        try: name = self.name
        except: name = ""
            
        return self.name
    
@receiver(post_save, sender=User)
def create_user_customer(sender, instance, created, **kwargs):
    if created:
        Customer.objects.create(user=instance, name='Anonymous')

@receiver(post_save, sender=User)
def save_user_customer(sender, instance, **kwargs):
    instance.customer.save()
    

class Category(models.Model): 
    name=models.CharField(max_length=100, blank=True, null=True)
    
    def __str__(self):
        return self.name
    

class Product(models.Model):
    name=models.CharField(max_length=250, null=True)
    price=models.DecimalField(max_digits=7, decimal_places=2)
    digital=models.BooleanField(default=False, null=True, blank=True)
    image=models.ImageField(null=True, blank=True, )
    category=models.ForeignKey(Category, on_delete=models.SET_NULL, blank=True, null=True)
    def __str__(self):
        return self.name
    
    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url
    
class Order(models.Model):
    customer=models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True)
    date_ordered=models.DateTimeField(auto_now_add=True)
    complete=models.BooleanField(default=False, null=True, blank=True)
    transaction_id=models.CharField(max_length=200, null=True)
    
    def __str__(self):
        return str(self.id)
    
    @property
    def get_cart_total(self):
        order_items = self.orderitem_set.all()
        total = sum([item.quantity for item in order_items])
        return total
        
    @property
    def get_cart_total_price(self):
        order_items = self.orderitem_set.all()
        total = sum([item.get_total for item in order_items])
        return total
    
    @property
    def shipping(self):
        order_items = self.orderitem_set.all()
        for item in order_items:
            # when at least one product is not digital, return True
            if not item.product.digital:
                return True
        return False
        
class OrderItem(models.Model):
    product=models.ForeignKey(Product, on_delete=models.SET_NULL, blank=True, null=True)
    order=models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
    quantity=models.IntegerField(default=0)
    date_added=models.DateTimeField(auto_now_add=True)
    
    @property
    def get_total(self):
        return self.product.price * self.quantity
    
class ShippingAddress(models.Model):
    customer=models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True)
    order=models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
    address=models.CharField(max_length=250, null=True)
    city=models.CharField(max_length=250, null=True)
    state=models.CharField(max_length=250, null=True)
    zipcode=models.CharField(max_length=250, null=True)
    date_added=models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.address
    
class Comment(models.Model):
    customer=models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True)
    product=models.ForeignKey(Product, on_delete=models.SET_NULL, blank=True, null=True)
    content=models.TextField(max_length=500)
    date_added=models.DateTimeField(auto_now_add=True)
    
class ProductRating(models.Model):
    customer=models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True)
    product=models.ForeignKey(Product, on_delete=models.SET_NULL, blank=True, null=True)
    value=models.IntegerField(default=0)

