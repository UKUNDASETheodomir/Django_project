from products import views
from .views import *
from django.urls import path



urlpatterns = [

      path("order/<int:id>/", place_order, name="place_order"),
      path("order/confirmation/<int:id>/", order_confirmation, name="order_confirmation"),
      path("my-orders/", customer_orders, name="customer_orders"),
       path('vendor/orders/', vendor_orders, name='vendor_orders'),
]



