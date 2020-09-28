from django.contrib import admin

# Register your models here.


from .models import Bag, OrderLineItem

admin.site.register(Bag)
admin.site.register(OrderLineItem)

