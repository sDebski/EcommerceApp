from django import forms

    
class ShippingForm(forms.Form):
    name = forms.CharField(max_length=200)
    email = forms.EmailField(required=True)
    address = forms.CharField(max_length=200)
    city = forms.CharField(max_length=200)
    state = forms.CharField(max_length=200)
    zipcode = forms.CharField(max_length=200)

