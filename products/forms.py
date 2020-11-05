from django import forms
from .models import Product, Category, Review, RATE_CHOICES


class AddProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'


class ReviewForm(forms.ModelForm):
    review = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': '3', }),
        required=False
    )
    rate = forms.ChoiceField(
        choices=RATE_CHOICES, widget=forms.Select(), required=True
    )

    class Meta:
        model = Review
        fields = ('review', 'rate')
