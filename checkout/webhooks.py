from django.http import HttpResponse
from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from .models import Order
from profiles.models import UserProfile
from shopping_bag.models import Bag
import time


import stripe


class StripeWebhook_Handler:
    """Handles webhooks from strip"""

    def __init__(self, request):
        self.request = request

    def handle_event(self, event):
        """
        Handles unknown or unexpected webhook event
        """
        return HttpResponse(
            content=f'Unhandled webhook received: {event["type"]}',
            status=200)

    def handle_payment_intent_succeeded(self, event):
        """
        Handles  payment_intent.succeeded webhook sent Stripe
        """
        intent = event.data.object
        payment_id = intent.id
        bag = intent.metadata.bag 
        print(bag)


        billing_details = intent.charges.data[0].billing_details
        shipping_details = intent.shipping
        grand_total = round(intent.charges.data[0].amount / 100, 2)

        # Clean data in the shipping details
        for field, value in shipping_details.address.items():
            if value == "":
                shipping_details.address[field] = None

        is_ordered = False
        attempt = 1
        while attempt <= 5:
            try:
                order = Order.objects.get(
                    full_name__iexact=shipping_details.name,
                    email__iexact=billing_details.email,
                    phone_number__iexact=shipping_details.phone,
                    country__iexact=shipping_details.address.country,
                    postcode__iexact=shipping_details.address.postal_code,
                    city__iexact=shipping_details.address.city,
                    address_1__iexact=shipping_details.address.line1,
                    address_2__iexact=shipping_details.address.line2,
                    state__iexact=shipping_details.address.state,
                    total=grand_total,
                    bag=bag,
                    stripe_paymentid=payment_id,
                )
                is_ordered = True
                break
            except Order.DoesNotExist:
                attempt += 1
                time.sleep(1)
        if is_ordered:
            return HttpResponse(
                content=f'Webhook received: {event["type"]} |\
                     SUCCESS: Verified order already in database',
                status=200)
        else:
            order = None
            try:
                order = Order.objects.create(
                    full_name=shipping_details.name,
                    email=billing_details.email,
                    phone_number=shipping_details.phone,
                    country=shipping_details.address.country,
                    postcode=shipping_details.address.postal_code,
                    city=shipping_details.address.city,
                    address_1=shipping_details.address.line1,
                    address_2=shipping_details.address.line2,
                    state=shipping_details.address.state,
                    bag=bag,
                    stripe_paymentid=payment_id,
                )
            except Exception as e:
                if order:
                    order.delete()
                return HttpResponse(
                    content=f'Webhook received: {event["type"]} | ERROR: {e}',
                    status=500)


        return HttpResponse(
            content=f'Webhook received: {event["type"]}',
            status=200)

    def handle_payment_intent_payment_failed(self, event):
        """
        Handles the payment_intent.payment_failed webhook sent Stripe
        """
        return HttpResponse(
            content=f'Webhook received: {event["type"]}',
            status=200)




@require_POST
@csrf_exempt
def webhook(request):
    """Listens for webhooks sent from Stripe"""
    wh_secret = settings.STRIPE_WH_SECRET
    stripe.api_key = settings.STRIPE_SECRET_KEY

    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(
        payload, sig_header, wh_secret
        )
    except ValueError as e:

        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:

        return HttpResponse(status=400)
    except Exception as e:
        return HttpResponse(content=e, status=400)

    handler = StripeWebhook_Handler(request)

    event_map = {
        'payment_intent.succeeded': handler.handle_payment_intent_succeeded,
        'payment_intent.payment_failed': handler.handle_payment_intent_payment_failed,
    }

    event_type = event['type']


    event_handler = event_map.get(event_type, handler.handle_event)

    response = event_handler(event)
    return response
