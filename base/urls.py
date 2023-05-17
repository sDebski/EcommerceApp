from . import views
from django.urls import path


urlpatterns = [
    path("", views.store, name='store'),
    path("register/", views.registerView, name='register'),
    path("login/", views.loginView, name='login'),
    path("logout/", views.logoutView, name='logout'),
    path("cart/", views.cart, name='cart'),
    path("checkout/", views.checkout, name='checkout'),
    path('update-item/', views.updateItem, name='update-item'),
    path('process-order/', views.processOrder, name='process-order'),
    path('view-item/<str:pk>', views.viewItem, name='view-item'),
    path('rating-item/<str:pk>/<str:value>', views.ratingItem, name='rating-item'),
    path('comment-item/<str:pk>', views.commentItem, name='comment'),
]
