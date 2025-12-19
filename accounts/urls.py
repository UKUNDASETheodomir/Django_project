from django.urls import path
from orders.views import customerOrder, vendor_orders  # Fixed import
from django.contrib.auth import views as auth_views
from products.views import *
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
    # path('orders/', vendor_orders, name='vendor_orders'),
    # path('customer_orders/', customerOrder, name='customer_orders'),
    path('my-products/', vendor_products, name='vendor_products'),
    path('my-reviews/', vendor_reviews, name='vendor_reviews'),
    path('create/', create_product, name='create_product'),
 
    path('edit/<int:id>/', edit_product, name='edit_product'),
    path('delete/<int:id>/', delete_product, name='delete_product'),
    
    path('login/', login_view, name='login'),
    path('login/verify/', verify_login_otp, name='verify_login_otp'),
    path('password-reset/', request_password_reset, name='request_password_reset'),
    path('password-reset/confirm/', reset_password_confirm, name='reset_password_confirm'),
    path('wishlist/add/<int:product_id>/', add_to_wishlist, name='add_to_wishlist'),
    path('wishlist/remove/<int:product_id>/', remove_from_wishlist, name='remove_from_wishlist'),
    path('wishlist/', wishlist_view, name='wishlist'),
    
    path('cart/', cart_view, name='cart'), 
    path('cart/add/<int:product_id>/', add_to_cart, name='add_to_cart'),
    path('cart/update/<int:item_id>/', update_cart_quantity, name='update_cart_quantity'),
    path('cart/remove/<int:item_id>/', remove_from_cart, name='remove_from_cart'),
]







