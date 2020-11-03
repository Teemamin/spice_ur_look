from django.urls import path
from . import views

urlpatterns = [
    path('', views.all_products, name='products'),
    path(
        '<int:product_id>/', views.single_product,
        name='single_product'
        ),
    path('add_product/', views.add_product, name='add_product'),
    path(
        'revise/<int:product_id>/', views.revise_product, name='revise_product'
    ),
    path(
        'delete_product/<int:product_id>/',
        views.delete_product, name='delete_product'
    ),
    path(
        'add_review/<product_id>/', views.add_review,
        name='add_review'
        ),
    path(
        'add_to_wishlist/', views.add_to_wishlist,
        name='add_to_wishlist'
        ),
    path(
        'wishlist_view/', views.wishlist_view, name='wishlist_view'
    ),
    path(
        'newsletter/', views.newsletter, name='newsletter'
    ),



]
