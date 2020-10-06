from django.urls import path
from . import views
from .webhooks import webhook

urlpatterns = [
    path('', views.checkout, name='checkout'),
    path(
        'success/<order_number>/',
        views.checkout_success, name='checkout_success'
        ),
    path('dump_bag_data/', views.dump_bag_data,
         name='dump_bag_data'),
    path('webhook/', webhook, name='webhook'),

]
