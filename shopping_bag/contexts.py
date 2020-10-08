from decimal import Decimal
from django.shortcuts import get_object_or_404
from .models import Bag



def bag_items(request):
    bag_id = request.session.get("bag_id", None)
    bag_obj, bag_created = Bag.objects.new_or_get(request)
    # bag_in_session = Bag.objects.filter(pk=bag_id)
    if bag_created or bag_obj.order_line_items.count() == 0:
        bag_in_session = None
    else:
        bag_in_session = bag_obj
   
    context = {
        'bag_in_session': bag_in_session,
    }

    return context
