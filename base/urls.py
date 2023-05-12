from . import views
from django.urls import path


urlpatterns = [
    path("", views.store, name='store'),
    path("cart/", views.cart, name='cart'),
    path("checkout/", views.checkout, name='checkout'),
    path('update-item/', views.updateItem, name='update-item'),
    path('process-order/', views.processOrder, name='process-order'),
    path('view-item/<str:pk>', views.viewItem, name='view-item')
   
]
