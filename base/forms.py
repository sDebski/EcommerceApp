from django import forms
from .models import *
from django.contrib.auth.forms import UserCreationForm

    
class ShippingForm(forms.Form):
    name = forms.CharField(max_length=200)
    email = forms.EmailField(required=True)
    address = forms.CharField(max_length=200)
    city = forms.CharField(max_length=200)
    state = forms.CharField(max_length=200)
    zipcode = forms.CharField(max_length=200)

class UserForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['username', 'password1','password2']

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['email', 'name']
        

