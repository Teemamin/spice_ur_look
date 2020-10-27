from django.contrib import admin
from .models import Product, Category, Review, Wishlist
# Register your models here.


class MyProductAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'category',
        'gender',
        'price',
        'image',
    )


class MyCategoryAdmin(admin.ModelAdmin):
    list_display = (
        'name',
    )


class ReviewAdmin(admin.ModelAdmin):
    list_display = ['rate', 'review', 'time_added']
    readonly_fields = ('review', 'user', 'product', 'rate', 'id')
    ordering = ('time_added',)


class WishlistAdmin(admin.ModelAdmin):
    list_display = ['user', 'wished_product', 'added_date']
    readonly_fields = ('user', 'wished_product', 'added_date')
    ordering = ('added_date',)


admin.site.register(Product, MyProductAdmin)
admin.site.register(Category, MyCategoryAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Wishlist, WishlistAdmin)
