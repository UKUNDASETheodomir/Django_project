from products import views
from .views import*
from django.urls import path

app_name = 'orders'  

urlpatterns = [

      path('create_order/', views.createOrder,name='create_order'),
]



