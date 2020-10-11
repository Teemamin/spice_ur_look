from django.shortcuts import render, redirect, reverse, get_object_or_404, HttpResponse
from .forms import CheckoutOrderForm
from .models import Order
from django.views.decorators.http import require_POST

from django.core import serializers

from django.conf import settings
from django.contrib import messages
from products.models import Product
from decimal import Decimal

import json
from shopping_bag.models import Bag
from profiles.models import UserProfile
import stripe

# Create your views here.


@require_POST
def order_data(request):
    try:
        pid = request.POST.get('client_secret').split('_secret')[0]
        stripe.api_key = settings.STRIPE_SECRET_KEY
        stripe.PaymentIntent.modify(pid, metadata={
            'bag': request.session.get("bag_id"),
            'username': request.user,
        })
        return HttpResponse(status=200)
    except Exception as e:
        messages.error(request, 'Sorry, your payment cannot be \
            processed right now. Please try again later.')
        return HttpResponse(content=e, status=400)


def checkout(request):
    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    stripe_secret_key = settings.STRIPE_SECRET_KEY
    bag_obj, bag_created = Bag.objects.new_or_get(request)
    order_obj = None
    if bag_created or bag_obj.order_line_items.count() == 0:
        return redirect('shopping_bag')
    current_bag = bag_obj
    delivery = Decimal(settings.FIXED_DELIVERY)
    total = current_bag.total + delivery
    stripe_total = round(total * 100)
    stripe.api_key = stripe_secret_key
    # creates payment intent
    intent = stripe.PaymentIntent.create(
        amount=stripe_total,
        currency=settings.STRIPE_CURRENCY,
    )

    if request.user.is_authenticated:
        try:
            profile = UserProfile.objects.get(user=request.user)
            checkoutorder_form = CheckoutOrderForm(initial={
                'full_name': profile.user.get_full_name(),
                'email': profile.user.email,
                'phone_number': profile.phone_number,
                'country': profile.country,
                'postcode': profile.postcode,
                'city': profile.city,
                'state': profile.state,
                'address_1': profile.street_address1,
                'address_2': profile.street_address2,
            })

        except UserProfile.DoesNotExist:
            checkoutorder_form = CheckoutOrderForm()
    else:
        checkoutorder_form = CheckoutOrderForm()
    if request.method == 'POST':
        order_bag = bag_obj
        orderform_data = {
            'full_name': request.POST['full_name'],
            'email': request.POST['email'],
            'phone_number': request.POST['phone_number'],
            'country': request.POST['country'],
            'postcode': request.POST['postcode'],
            'city': request.POST['city'],
            'address_1': request.POST['address_1'],
            'address_2': request.POST['address_2'],
            'state': request.POST['state'],
        }
        checkoutorder_form = CheckoutOrderForm(orderform_data)
        if checkoutorder_form.is_valid:
            order = checkoutorder_form.save(commit=False)
            order.bag = order_bag
            stripe_paymentid = request.POST.get('client_secret').split('_secret')[0]
            order.stripe_paymentid = stripe_paymentid
            # order_obj = Order.objects.new_or_get(order_bag)
            # print(f'{order_obj} frm order_obj')
            if request.user.is_authenticated:
                profile = UserProfile.objects.get(user=request.user)
                order.user_profile = profile
            order.save()

            return redirect(reverse('checkout_success',
                            args=[order.order_number]))
        else:
            messages.error(request, 'error processing your form. \
                Please double check the info provided.')
    context = {
        'checkoutorder_form': checkoutorder_form,
        'bag_obj': bag_obj,
        'stripe_public_key': stripe_public_key,
        'client_secret': intent.client_secret,
    }
    return render(request, 'checkout/checkout.html', context)


def checkout_success(request, order_number):
    order = get_object_or_404(Order, order_number=order_number)
    messages.success(request, f'Order successfully processed! \
        Your order number is {order_number}. A confirmation \
        email will be sent to {order.email}.')
    if 'bag_id' in request.session:
        del request.session['bag_id']
    context = {
        'order': order,
    }
    return render(request, "checkout/checkout_success.html", context)
