from django import forms
from .models import Order


class CheckoutOrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ('full_name', 'email', 'phone_number',
                  'address_1', 'address_2',
                  'city', 'state', 'postcode', 'country',
                  )
