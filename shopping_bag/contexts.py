from .models import Bag


def bag_items(request):
    bag_obj, bag_created = Bag.objects.new_or_get(request)
    bag_total = bag_obj.total
    context = {
        'bag_total': bag_total,
    }

    return context
