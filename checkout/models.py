from django.db import models
import uuid
import math
from django.db.models.signals import post_save, pre_save
from django.conf import settings


from profiles.models import UserProfile
from shopping_bag.models import Bag
from django_countries.fields import CountryField


# Create your models here.

class OrderManager(models.Manager):
    def new_or_get(self, bag_obj):
        created = False
        qs = self.get_queryset().filter(
                bag=bag_obj,
                active=True,
                order_status='created'
                )
        if qs.count() == 1:
            obj = qs.first()
        else:
            obj = self.model.objects.create(
                    bag=bag_obj,
                    )
            created = True
        return obj, created


ORDER_STATUS = (
    ('created', 'Created'),
    ('paid', 'Paid'),
)


class Order(models.Model):
    order_number = models.CharField(max_length=32, null=False, editable=False)
    user_profile = models.ForeignKey(
        UserProfile, on_delete=models.SET_NULL,
        null=True, blank=True, related_name='orders'
    )
    full_name = models.CharField(max_length=60, null=False, blank=False)
    bag = models.ForeignKey(Bag, on_delete=models.CASCADE)
    order_status = models.CharField(
        max_length=50, default='created', choices=ORDER_STATUS
        )
    email = models.EmailField(max_length=200, null=False, blank=False)
    phone_number = models.CharField(max_length=20, null=False, blank=False)
    address_1 = models.CharField(max_length=90, null=False, blank=False)
    address_2 = models.CharField(max_length=90, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    city = models.CharField(max_length=120)
    state = models.CharField(max_length=120, blank=True)
    postcode = models.CharField(max_length=20, blank=True)
    country = CountryField(null=False, blank=False)
    stripe_paymentid = models.CharField(
        max_length=270, null=False, blank=False, default=''
    )

    delivery_total = models.DecimalField(
        default=0, max_digits=7, decimal_places=2
        )
    total = models.DecimalField(default=0.00, max_digits=100, decimal_places=2)
    active = models.BooleanField(default=True)

    def _generate_order_number(self):
        """
        Generate a random, unique order number using UUID
        """
        return uuid.uuid4().hex.upper()

    def update_total(self):
        bag_total = self.bag.total
        self.delivery_total = settings.FIXED_DELIVERY
        delivery_total = self.delivery_total
        grand_total = math.fsum([bag_total, delivery_total])
        total_formated = format(grand_total, '.2f')
        self.total = total_formated
        self.save()
        return total_formated

    def save(self, *args, **kwargs):
        """
        Set the order number if it hasn't been set already.
        """
        if not self.order_number:
            self.order_number = self._generate_order_number()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.order_number

    objects = OrderManager()


def pre_save_create_order_id(sender, instance, *args, **kwargs):
    qs = Order.objects.filter(bag=instance.bag)
    if qs.exists():
        qs.update(active=False)


pre_save.connect(pre_save_create_order_id, sender=Order)

def post_save_bag_total(sender, instance, created, *args, **kwargs):
    if not created:
        bag_obj = instance
        bag_total = bag_obj.total
        bag_id = bag_obj.id
        queryset = Order.objects.filter(bag__id=bag_id)
        if queryset.count() == 1:
            order_obj = queryset.first()
            order_obj.update_total()


post_save.connect(post_save_bag_total, sender=Bag)


def post_save_bag_order(sender, instance, created, *args, **kwargs):
    if created:
        instance.update_total()


post_save.connect(post_save_bag_order, sender=Order)
