from django.contrib import admin
from .models import Order
# Register your models here.


class CheckoutOrderAdmin(admin.ModelAdmin):
    readonly_fields = ('order_number', 'date',
                       'delivery_total', 'total', 'bag',)
    fields = (
        'order_number', 'user_profile', 'full_name',
        'email', 'phone_number', 'address_1', 'address_2',
        'city', 'state', 'postcode', 'country', 'delivery_total',
        'total', 'bag',
            )

    list_display = ('order_number', 'date', 'full_name',
                    'total', 'delivery_total',
                    )

    ordering = ('-date',)


admin.site.register(Order, CheckoutOrderAdmin)
