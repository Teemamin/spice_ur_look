from django.urls import path
from . import views

urlpatterns = [
    path('', views.all_products, name='products'),
    path(
        '<int:product_id>/', views.single_product,
        name='single_product'
        ),
    path('add_product/', views.add_product, name='add_product'),
    path('revise/<int:product_id>/', views.revise_product, name='revise_product'),
    path('delete_product/<int:product_id>/', views.delete_product, name='delete_product'),



]
