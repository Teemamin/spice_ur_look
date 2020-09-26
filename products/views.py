from django.shortcuts import render, redirect, reverse
from .models import Product, Category
from django.contrib import messages
from django.db.models import Q

# Create your views here.


def all_products(request):
    products = Product.objects.all()
    if request.GET:
        if 'gender' in request.GET:
            gender = request.GET['gender']
            products = products.filter(gender=gender)
        if 'search' in request.GET:
            search_word = request.GET['search']
            if not search_word:
                messages.error(request, "please enter a message")
                return redirect(reverse('products'))
            search_words = Q(name__icontains=search_word) |\
                Q(description__icontains=search_word)\
                | Q(color__icontains=search_word)
            products = products.filter(search_words)
    context = {
        'products': products,
        'search_word': search_word,

    }
    return render(request, 'products/products.html', context)
