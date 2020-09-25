from django.shortcuts import render
from .models import Product, Category

# Create your views here.


def all_products(request):
    products = Product.objects.all()
    if request.GET:
        if 'gender' in request.GET:
            gender = request.GET['gender']
            products = products.filter(gender=gender)
    context = {
        'products': products,

    }
    return render(request, 'products/products.html', context)
