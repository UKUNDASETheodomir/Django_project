from django.shortcuts import redirect, render

from accounts.models import CustomUser
from orders.form import OrderForm
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
def createOrder(request):
    form = OrderForm
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            form.save()
            
    context = {'form':form}
    return render(request, 'order_form.html',context)

def updateOrder(request,pk ):
    order = Order.objects.get(id=pk)
    form = OrderForm(instance = order)   
    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('home')

    context = {'form':form}
    return render(request, 'order_form.html',context)

def deleteOrder(request,pk):
    order = Order.objects.get(id=pk)
    if request.method == "POST":
        order.delete() 
        return redirect("/")
    
    context = {'item':order}
    return render(request, 'delete.html',context)