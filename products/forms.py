from django import forms
from .models import Product, Category


class AddProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'