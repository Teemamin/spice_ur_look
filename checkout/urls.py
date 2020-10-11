from django.urls import path
from . import views
from .webhooks import webhook

urlpatterns = [
    path('', views.checkout, name='checkout'),
    path(
        'success/<order_number>/',
        views.checkout_success, name='checkout_success'
        ),
    path('order_data/', views.order_data,
        name='cache_checkout_data'),
    path('webhook/', webhook, name='webhook'),

]
