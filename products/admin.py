from django.contrib import admin
from .models import Product, Category, Review
# Register your models here.


class MyProductAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'category',
        'gender',
        'price',
        'rating',
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


admin.site.register(Product, MyProductAdmin)
admin.site.register(Category, MyCategoryAdmin)
admin.site.register(Review, ReviewAdmin)

