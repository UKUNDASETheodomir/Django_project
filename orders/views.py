from django.shortcuts import render

from accounts.models import CustomUser
from .models import*

def vendorOrder(request):
    orders=Order.objects.all()
    customers= CustomUser.objects.all()
    total_customers = customers.count()
    total_orders = orders.count()
    paid = orders.filter(status='paid').count()
    pending = orders.filter(status='pending').count() 
    active = orders.filter(status='active').count()  
    context = {'orders':orders, 'customers':customers, 'total_orders': total_orders, 'paid': paid, 'pending': pending, 'active': active} 
    return render(request, "vend_order.html", context)
def customerOrder(request):
    orders=Order.objects.all()
    customers= CustomUser.objects.all()
    total_customers = customers.count()
    vendors= CustomUser.objects.filter(user_type='V')
    total_vendors = vendors.count()
    total_orders = orders.count()
    paid = orders.filter(status='paid').count()
    pending = orders.filter(status='pending').count() 
    active = orders.filter(status='active').count()  
    context = {'orders':orders, 'customers':customers, 'total_vendors': total_vendors, 'total_orders': total_orders, 'paid': paid, 'pending': pending, 'active': active} 
    return render(request, "customer_order.html", context)