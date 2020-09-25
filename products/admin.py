from django.contrib import admin
from .models import Product, Category
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


admin.site.register(Product, MyProductAdmin)
admin.site.register(Category, MyCategoryAdmin)
