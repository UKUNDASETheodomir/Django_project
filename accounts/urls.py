from django.urls import path
from .views import register_view, login_view, logout_view,home_view,dashboard,vendor_dashboard

urlpatterns = [
     path('', home_view, name='home'),  # <-- home page
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('dashboard/', dashboard, name='dashboard'),
     path('dashboard/vendor/',vendor_dashboard, name='vendor_dashboard'),
     path('home/', home_view, name='home'),
]
