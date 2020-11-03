from django.shortcuts import render,\
     redirect, get_object_or_404, reverse
from products.models import Product
from .models import Bag, OrderLineItem
from django.contrib import messages
from django.conf import settings

# Create your views here.


def calc_bag(bag_obj):
    """custom method to calc shopping bag to total"""
    order_line_items = bag_obj.order_line_items.all()
    total = 0
    for x in order_line_items:
        total += x.product.price * x.quantity
    bag_obj.subtotal = total
    bag_obj.total = float(total) + float(settings.FIXED_DELIVERY)
    bag_obj.save()


def shopping_bag(request):
    """
    A view to display shopping bag content
    """
    bag_obj, new_obj = Bag.objects.new_or_get(request)
    context = {
        'bag': bag_obj
    }
    return render(request, 'shopping_bag/shopping_bag.html', context)


def add_to_shopping_bag(request):
    """
    A view that adds quantity of the specified product
    to the shopping bag, updates size and cost acoordingly
    """
    product_id = request.POST.get('product_id')
    redirect_url = request.POST.get('redirect_url')
    quantity = int(request.POST.get('quantity'))
    size = None
    if 'itm_size' in request.POST:
        size = request.POST['itm_size']

    if product_id is not None:
        try:
            product_obj = Product.objects.get(id=product_id)
            product_obj.size = size
        except Product.DoesNotExist:
            messages.error(request, 'Product not found')
            return redirect(redirect_url)
        bag_obj, new_obj = Bag.objects.new_or_get(request)

        if bag_obj.order_line_items.filter(product=product_obj):
            bag_prod_objs = bag_obj.order_line_items.filter(
                product=product_obj, product_size=size
            )
            if bag_prod_objs:
                bag_prod_obj = bag_prod_objs[0]
                if bag_prod_obj.product_size == size:
                    bag_prod_obj.quantity += quantity
                    bag_prod_obj.save()
            else:
                bag_obj.order_line_items.create(
                    product=product_obj, product_size=size, quantity=quantity
                )
        else:
            bag_obj.order_line_items.create(
                product=product_obj, product_size=size, quantity=quantity
            )
        calc_bag(bag_obj)
    return redirect('shopping_bag')


def alter_shoping_bag(request, item_id):
    """
    Alters the quantity of the specified product
    to the specified amount and ajusts the cost
    accordingly
    """
    product_obj = Product.objects.get(pk=item_id)
    quantity = int(request.POST.get('quantity'))
    bag_id = request.session.get("bag_id")
    bag_obj = Bag.objects.get(pk=bag_id)
    try:
        bag_filtered = bag_obj.order_line_items.filter(product=product_obj)
        bag_prod_obj = bag_filtered[0]
        bag_prod_obj.quantity = quantity
        bag_prod_obj.save()
        calc_bag(bag_obj)
        messages.success(request, 'product updated successfully!')
        return redirect(reverse('shopping_bag'))
    except Exception as e:
        messages.error(request, f'Error updating product: {e}')
        return redirect(reverse('shopping_bag'))


def remove_from_bag(request, product_id):
    """
    Deletes the specified product from the shopping bag
    """
    product_obj = get_object_or_404(OrderLineItem, pk=product_id)
    bag_obj, new_obj = Bag.objects.new_or_get(request)
    bag_obj.order_line_items.remove(product_obj)
    return redirect('shopping_bag')
