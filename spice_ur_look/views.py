from django.shortcuts import render
from products.models import Product
from products.models import Wishlist


def home(request):
    """
    Displays products under the new arrival category
    """
    products = Product.objects.filter(category__name="new_arrivals")
    current_user_prdct_id = []
    whishlist_obj = Wishlist.objects.all()
    if request.user.is_authenticated:
        current_user_whishlist = whishlist_obj.filter(user=request.user)
        for itm in current_user_whishlist:
            current_user_prdct_id.append(itm.wished_product.id)
    context = {
        'products': products,
        'current_user_prdct_id': current_user_prdct_id,
    }
    return render(request, 'index.html', context)
