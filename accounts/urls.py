from django.urls import path
from orders.views import customerOrder, vendorOrder
from products.views import create_product, vendor_products
from .views import *
urlpatterns = [
    path('', home_view, name='home'),  # <-- home page
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('add_product/', create_product, name='add_product'),
    path('dashboard/', dashboard, name='dashboard'),
    path('dashboard/vendor/',vendor_dashboard, name='vendor_dashboard'),
    path('home/', home_view, name='home'),
    path('products/', product_list, name='product_list'),
    path('products/<int:id>/', product_detail, name='product_detail'),
    path('user/', userPage, name='user'),
    path('orders/', vendorOrder, name='vendor_orders'),
    path('customer_orders/', customerOrder, name='customer_orders'),
    # path('home_page/', HomePage, name='home_page'),
    path('my-products/', vendor_products, name='vendor_products'),
    path('create/', create_product, name='create_product'),
]

