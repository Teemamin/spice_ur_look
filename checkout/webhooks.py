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
        print(payment_id)

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
