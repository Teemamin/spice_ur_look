from django.db import models
from decimal import Decimal
from django.conf import settings
from django.db.models.signals import pre_save, post_save, m2m_changed
from products.models import Product
from django.core import serializers

# Create your models here.
User = settings.AUTH_USER_MODEL


class BagManager(models.Manager):
    def new_or_get(self, request):
        bag_id = request.session.get("bag_id", None)
        current_bag = request.session.get("current_bag", None)

        qs = self.get_queryset().filter(id=bag_id)
        if qs.count() == 1:
            new_obj = False
            bag_obj = qs.first()
            if request.user.is_authenticated and bag_obj.user is None:
                bag_obj.user = request.user
                bag_obj.save()
            data = serializers.serialize("json", [bag_obj], ensure_ascii=False)
            data_result = data[1:-1]

            request.session["current_bag"] = data_result
        else:
            bag_obj = Bag.objects.new(user=request.user)
            new_obj = True
            request.session["bag_id"] = bag_obj.id

        return bag_obj, new_obj

    def new(self, user=None):
        user_obj = None
        if user is not None:
            if user.is_authenticated:
                user_obj = user
        return self.model.objects.create(user=user_obj)


class OrderLineItem(models.Model):
    product = models.ForeignKey(
        Product, null=False, blank=False, on_delete=models.CASCADE
    )
    product_size = models.CharField(
        max_length=2,  blank=True, null=True
    )  # XS, S, M, L, XL
    quantity = models.IntegerField(null=False, blank=False, default=0)

    def __str__(self):
        return str(self.product)


class Bag(models.Model):
    user = models.ForeignKey(
        User, null=True, blank=True, on_delete=models.CASCADE
    )
    order_line_items = models.ManyToManyField(OrderLineItem, blank=True)
    subtotal = models.DecimalField(
        default=0.00, max_digits=100, decimal_places=2
    )
    total = models.DecimalField(
        default=0.00, max_digits=100, decimal_places=2
    )
    updated = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    objects = BagManager()

    def __str__(self):
        return str(self.id)


def m2m_changed_bag_receiver(sender, instance, action, *args, **kwargs):
    if action == 'post_add' or action == 'post_remove'\
         or action == 'post_clear':
        order_line_items = instance.order_line_items.all()
        total = 0
        for x in order_line_items:
            total += x.product.price * x.quantity
        instance.subtotal = total
        instance.total = total
        instance.save()


m2m_changed.connect(
    m2m_changed_bag_receiver, sender=Bag.order_line_items.through
)

