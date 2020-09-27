from django.shortcuts import render, redirect, reverse, get_object_or_404
from .models import Product, Category
from django.db.models.functions import Lower
from django.contrib import messages
from django.db.models import Q

# Create your views here.


def all_products(request):
    products = Product.objects.all()
    search_word = None
    categories = None
    cat = None
    sort = None
    direction = None
    if request.GET:
        if 'gender' in request.GET:
            gender = request.GET['gender']
            products = products.filter(gender=gender)
        if 'cat' in request.GET:
            cat = request.GET['cat'].split(',')
            if 'gender' in request.GET:
                gender = request.GET['gender'].split(',')
            #     print(gender)
            products = products.filter(category__name__in=cat)
            categories = Category.objects.filter(name__in=cat)
        if 'search' in request.GET:
            search_word = request.GET['search']
            if not search_word:
                messages.error(request, "please enter a message")
                return redirect(reverse('products'))
            search_words = Q(name__icontains=search_word) |\
                Q(description__icontains=search_word)\
                | Q(color__icontains=search_word)
            products = products.filter(search_words)

        if 'arrange' in request.GET:
            sort_word = request.GET['arrange']
            sort = sort_word
            if sort_word == 'name':
                sort_word = 'lower_name'
                products = products.annotate(lower_name=Lower('name'))

            if sort_word == 'category':
                sort_word = 'category__name'

            if 'direction' in request.GET:
                direction = request.GET['direction']
                if direction == 'desc':
                    sort_word = f'-{sort_word}'
            products = products.order_by(sort_word)
    sorting = f'{sort}_{direction}'
    context = {
        'products': products,
        'categories': categories,
        'search_word': search_word,
        'sorting': sorting,

    }
    return render(request, 'products/products.html', context)



def single_product(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    # bag_obj, new_obj = Bag.objects.new_or_get(request)
    context = {
        'product': product,
        # 'cart': bag_obj
    }
    return render(request, 'products/single_product.html', context)

