from django.shortcuts import render, redirect,\
     reverse, get_object_or_404, HttpResponse
from .forms import CheckoutOrderForm
from .models import Order
from django.views.decorators.http import require_POST

from django.conf import settings
from django.contrib import messages
from decimal import Decimal


from shopping_bag.models import Bag
from profiles.models import UserProfile
import stripe

# Create your views here.


@require_POST
def order_data(request):
    """
    Gets post data from stripe js before payment confirmation,
    allows us to attch the bag and user making the purchase to
    stripe payment data
    """
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
    """
    Gets stripe keys,checks if shopping bag in session is empty:
    if so: it redirects shopping_bag page, else if not empty:
    gets the existing shopping bag and calculates the total cost
    of items and creates a stripe payment intent. if a user is
    authenticated: it attempts to populate the checkout form
    with the user profile details else it renders and empty
    checkout form.
    post requests: collects form data, if valid: attaches the
    bag that created the order and stripe payment id to the order model
    if user is authenticated: it adds the order to their profile aswell
    finally it redirects to success page with order-number as argument
    """
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
            stripe_paymentid = request.POST.get(
                'client_secret').split('_secret')[0]
            order.stripe_paymentid = stripe_paymentid
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
    """
    gets order object and render order details,
    deletes bag in session
    """
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
