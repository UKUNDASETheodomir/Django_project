from .views import*
from django.urls import path

app_name = 'orders'  

urlpatterns = [
     path('orders/', vendorOrder, name='vendor_orders'),
      
]



