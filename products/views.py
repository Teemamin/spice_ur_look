from django.shortcuts import render, redirect, reverse, get_object_or_404, HttpResponseRedirect
from .models import Product, Category, Review, Wishlist
from django.db.models.functions import Lower
from django.contrib import messages
from django.db.models import Q
from shopping_bag.models import Bag
from profiles.models import UserProfile
from checkout.models import Order

from .forms import AddProductForm, ReviewForm
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


def single_product(request, product_id, *args, **kwargs):
    product = get_object_or_404(Product, pk=product_id)
    bag_obj, new_obj = Bag.objects.new_or_get(request)
    user_order_prdct_id = []
    current_user_prdct_id = []
    whishlist_obj = Wishlist.objects.all()
    profile = None
    profile_orders = None
    if request.user.is_authenticated:
        profile = get_object_or_404(UserProfile, user=request.user)
        profile_orders = profile.orders.all()
        for order in profile_orders:
            for item in order.bag.order_line_items.all():
                user_order_prdct_id.append(item.product.id)
        current_user_whishlist = whishlist_obj.filter(user=request.user)
        for itm in current_user_whishlist:
            current_user_prdct_id.append(itm.wished_product.id)
    review_obj = Review.objects.all().order_by('-time_added',)
    review_count = review_obj.filter(product_id=product_id).count()
    review_form = ReviewForm()
    context = {
        'product': product,
        'bag': bag_obj,
        'review_form': review_form,
        'review_obj': review_obj,
        'review_count': review_count,
        'profile_orders': profile_orders,
        'user_order_prdct_id': user_order_prdct_id,
        'current_user_prdct_id': current_user_prdct_id,
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


def add_review(request, product_id):
    product_obj = Product.objects.get(pk=product_id)
    redirect_url = request.POST.get('redirect_url')
    url = request.META.get('HTTP_REFERER')
    if request.method == 'POST':
        review_form_data = {
            'review': request.POST['review'],
            'rate': request.POST['rate'],
        }
        review_form = ReviewForm(review_form_data)
        if review_form.is_valid:
            review = review_form.save(commit=False)
            review.user = request.user
            review.product = product_obj
            review.save()
            messages.success(
                request, "Your review has ben sent.\
                    We appreciate your feedback!."
            )
            return HttpResponseRedirect(url)

    return HttpResponseRedirect(url)



def add_to_wishlist(request):
    url = request.META.get('HTTP_REFERER')
    if request.is_ajax() and request.POST and 'attr_id' in request.POST:
        if request.user.is_authenticated:
            data = Wishlist.objects.filter(
                user_id=request.user.pk,
                wished_product_id=int(request.POST['attr_id'])
            )
            if data.exists():
                data.delete()
            else:
                Wishlist.objects.create(
                    user_id=request.user.pk,
                    wished_product_id=int(request.POST['attr_id'])
                )
    else:
        print("No Product is Found")

    return HttpResponseRedirect(url)


