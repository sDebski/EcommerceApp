from django.contrib import admin
from .models import *


admin.site.register(Customer)
admin.site.register(ShippingAddress)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Comment)
admin.site.register(ProductRating)
admin.site.register(Category)
# Register your models here.
