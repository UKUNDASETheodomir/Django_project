from django.urls import path
from .views import product_list, create_product, vendor_products

urlpatterns = [
    path('', product_list, name='product_list'),
    
    
    
    
    
]
