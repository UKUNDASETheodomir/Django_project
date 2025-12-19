
from products import views
from .views import *

from .views import*
from django.urls import path



urlpatterns = [


      path("order/<int:id>/", place_order, name="place_order"),
      path("checkout/", checkout, name="checkout"),
      path("order/confirmation/<int:id>/", order_confirmation, name="order_confirmation"),
      path("my-orders/", customer_orders, name="customer_orders"),
      path('vendor/orders/', vendor_orders, name='vendor_orders'),
      path('vendor/order/<int:order_id>/', vendor_order_detail, name='vendor_order_detail'),
      path('my-orders/<int:order_id>/', customer_order_detail, name='customer_order_detail'),
      path('payment/<int:order_id>/', payment, name='payment'),
      path('payment-success/', payment_success, name='payment_success'),

     # path('orders/', vendorOrder, name='vendor_orders'),
     # path('customer_orders/', customerOrder, name='customer_orders'),

]



