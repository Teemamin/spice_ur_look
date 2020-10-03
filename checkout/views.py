from django.shortcuts import render, redirect, reverse
from .forms import CheckoutOrderForm
from .models import Order
from django.conf import settings
from django.contrib import messages


from shopping_bag.models import Bag
from profiles.models import UserProfile
import stripe

# Create your views here.


def checkout(request):
    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    stripe_secret_key = settings.STRIPE_SECRET_KEY
    bag_obj, bag_created = Bag.objects.new_or_get(request)
    order_obj = None
    if bag_created or bag_obj.order_line_items.count() == 0:
        return redirect('shopping_bag')
    current_bag = bag_obj
    total = current_bag.total
    stripe_total = round(total * 100)
    stripe.api_key = stripe_secret_key
    # creates payment intent
    intent = stripe.PaymentIntent.create(
        amount=stripe_total,
        currency=settings.STRIPE_CURRENCY,
    )
    print(intent)

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
            if request.user.is_authenticated:
                profile = UserProfile.objects.get(user=request.user)
                order.user_profile = profile
            order.save()
            return redirect(reverse('checkout_success'))
    context = {
        'checkoutorder_form': checkoutorder_form,
        'bag_obj': bag_obj,
        'stripe_public_key': stripe_public_key,
        'client_secret': intent.client_secret,
    }
    return render(request, 'checkout/checkout.html', context)


def checkout_success(request):
    context = {

    }
    return render(request, "checkout/checkout_success.html", context)
