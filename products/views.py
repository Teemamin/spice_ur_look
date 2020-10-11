from django.shortcuts import render, redirect, reverse, get_object_or_404
from .models import Product, Category
from django.db.models.functions import Lower
from django.contrib import messages
from django.db.models import Q
from shopping_bag.models import Bag
from .forms import AddProductForm
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


def single_product(request, product_id,*args, **kwargs):
    product = get_object_or_404(Product, pk=product_id)
    bag_obj, new_obj = Bag.objects.new_or_get(request)
    context = {
        'product': product,
        'bag': bag_obj
    }
    return render(request, 'products/single_product.html', context)


def add_product(request):
    """ Add a product to the store """
    if not request.user.is_superuser:
        messages.error(request, 'Access denied!.')
        return redirect(reverse('home'))

    if request.method == 'POST':
        form = AddProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save()
            messages.success(request, 'Product added successfully!')
            return redirect(reverse('single_product', args=[product.id]))
        else:
            messages.error(request, 'Error proceesing your form, kindly check\
                 your inputs are valid.')
    else:
        form = AddProductForm()

    context = {
        'form': form,
    }

    return render(request, 'products/add_product.html', context)

def revise_product(request, product_id):
    """ Edits and updates a product in the site """
    if not request.user.is_superuser:
        messages.error(request, 'Access denied!.')
        return redirect(reverse('home'))

    product = get_object_or_404(Product, pk=product_id)
    if request.method == 'POST':
        form = AddProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product successfully revised!')
            return redirect(reverse('single_product', args=[product.id]))
        else:
            messages.error(request, 'Error proceesing your form, kindly check\
                your inputs are valid.')
    else:
        form = AddProductForm(instance=product)
        messages.info(request, f'You are revising {product.name}')

    context = {
        'form': form,
        'product': product,
    }

    return render(request, 'products/revise_product.html', context)


def delete_product(request, product_id):
    """ Deletes  product from the site """
    if not request.user.is_superuser:
        messages.error(request, 'Access denied.')
        return redirect(reverse('home'))

    product = get_object_or_404(Product, pk=product_id)
    product.delete()
    messages.success(request, 'Successfully deleted product!')
    return redirect(reverse('products'))