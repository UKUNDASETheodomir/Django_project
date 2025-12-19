from django.shortcuts import render, get_object_or_404, redirect
from django.conf import settings
from .form import OrderForm
from .models import Order, OrderItem
from products.models import product, Cart, CartItem
from django.shortcuts import render
from accounts.models import CustomUser
from .models import*
from django.contrib.auth.decorators import login_required
from accounts.decorators import customer_required,vendor_required

@login_required(login_url='login')
@customer_required
def place_order(request, id):
    product_obj = get_object_or_404(product,id=id)

    if request.method == "POST":
        form = OrderForm(request.POST)
        quantity = int(request.POST.get("quantity"))  # coming from template input

        if form.is_valid():

            
            # 1. Create main order
            order = form.save(commit=False)
            order.customer = request.user
            order.status = "PENDING"
            order.total = product_obj.price * quantity
            order.save()

            print("ORDER CREATED:", order.id)
            # 2. Create order item
            OrderItem.objects.create(
                order=order,
                product=product_obj,
                quantity=quantity,
                price=product_obj.price
            )

            return redirect("payment", order_id=order.id)
  

    else:
        form = OrderForm()

    return render(request, "orders/place_order.html", {
        "form": form,
        "product": product_obj
    })
def order_confirmation(request, id):
    
    order = get_object_or_404(Order, id=id, customer=request.user)
    order_items = OrderItem.objects.filter(order=order)

    return render(request, "orders/order_confirmation.html", {
        "order": order,
        "order_items": order_items

    })
def customer_orders(request):
    # only get orders for the logged-in user
    orders = Order.objects.filter(customer=request.user).order_by('-created_at')
    
    context = {
        "orders": orders
    }
    return render(request, "orders/customer_orders.html", context)
@login_required(login_url='login')
@customer_required
def customer_order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id, customer=request.user)
    items = order.orderitem_set.all()
    
    context = {
        'order': order,
        'items': items,
    }
    return render(request, 'orders/customer_order_detail.html', context)

from decimal import Decimal

@login_required(login_url='login')
@vendor_required
def vendor_orders(request):
    vendor = request.user

    # get distinct orders from these items
    orders = Order.objects.filter(orderitem__product__vendor=vendor).distinct().order_by('-created_at')
    
    orders_with_totals = []
    for order in orders:
        total = Decimal('0.00')
        vendor_items = []
        for item in order.orderitem_set.all():
            if item.product.vendor == vendor:
                total += item.line_total
                item.view_total = item.line_total # item.line_total is a property, view_total is safe as a dynamic attr
                vendor_items.append(item)
        print(f"DEBUG: Order {order.id} for Vendor {vendor.username} has {len(vendor_items)} items. Total: {total}")
        orders_with_totals.append({
            "order": order,
            "items": vendor_items,
            "total": total
        })

    print(f"DEBUG: Returning {len(orders_with_totals)} orders with totals.")

    context = {
        "orders_with_totals": orders_with_totals,
        "vendor": vendor,
    }
    return render(request, "orders/vendor_orders.html", context)

@login_required(login_url='login')
@vendor_required
def vendor_order_detail(request, order_id):
    vendor = request.user
    order = get_object_or_404(Order, id=order_id)
    
    # Only get items belonging to this vendor
    items = order.orderitem_set.filter(product__vendor=vendor)
    
    if not items.exists():
        messages.error(request, "Access denied. This order does not contain your products.")
        return redirect('vendor_orders')
        
    # Mark as viewed by this vendor
    if request.user not in order.viewed_by.all():
        order.viewed_by.add(request.user)
        
    total_earnings = sum(item.line_total for item in items)

    context = {
        'order': order,
        'items': items,
        'total_earnings': total_earnings,
    }
    return render(request, 'orders/vendor_order_detail.html', context)


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
    customers = CustomUser.objects.filter(user_type='C')
    total_orders = orders.count()
    paid = orders.filter(status='paid').count()
    pending = orders.filter(status='pending').count() 
    active = orders.filter(status='active').count()  
    context = {'orders':orders, 'customers':customers,  'total_orders': total_orders, 'paid': paid, 'pending': pending, 'active': active} 
    return render(request, "customer_order.html", context)


from django.db.models import Sum, F, DecimalField

@login_required(login_url='login')
@customer_required
def checkout(request):
    """
    Handles the Checkout process for the entire Cart.
    """
    if request.method == "POST":
        form = OrderForm(request.POST) 
        if form.is_valid():
            cart = Cart.objects.get(user=request.user)
            cart_items = CartItem.objects.filter(cart=cart)
            
            # 1. Calc total again for safety
            total = sum(item.product.price * item.quantity for item in cart_items)
            
            # 2. Create Order
            order = form.save(commit=False)
            order.customer = request.user
            order.status = "PENDING"
            order.total = total
            order.save()
            
            # 3. Create Order Items
            for item in cart_items:
                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    quantity=item.quantity,
                    price=item.product.price
                )

            # 4. Clear Cart
            cart_items.delete()
            # Optional: Delete cart itself or just items. Usually clearing items is enough.
            
            return redirect("payment", order_id=order.id)
            
    else:
        form = OrderForm()
        
    # Get Cart Data for display
    try:
        cart = Cart.objects.get(user=request.user)
        cart_items = CartItem.objects.filter(cart=cart)
        total = sum(item.product.price * item.quantity for item in cart_items)
    except Cart.DoesNotExist:
        cart_items = []
        total = 0
        
    return render(request, "orders/checkout.html", {
        "form": form,
        "cart_items": cart_items,
        "total": total
    })

def payment(request, order_id):
    order = get_object_or_404(Order, id=order_id, customer=request.user)
    return render(request, "orders/payment.html", {
        "order": order,
        "PAYPAL_CLIENT_ID": settings.PAYPAL_CLIENT_ID
    })

import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

def payment_success(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        order_id = data.get('orderID')
        trans_id = data.get('transID')
        
        # Verify order and update status
        try:
            order = Order.objects.get(id=order_id)
            order.status = 'PAID'
            
            # REDUCE STOCK ON SUCCESSFUL PAYMENT
            for item in order.orderitem_set.all():
                if item.product.stock >= item.quantity:
                    item.product.stock -= item.quantity
                    item.product.save()
                else:
                    # Optional: Handle overselling scenario if necessary
                    # For now just subtract and go negative or stop at 0
                    item.product.stock = max(0, item.product.stock - item.quantity)
                    item.product.save()

            order.save()
            return JsonResponse({'message': 'Payment successful', 'status': 'success'})
        except Order.DoesNotExist:
            return JsonResponse({'message': 'Order not found', 'status': 'error'}, status=404)
    return JsonResponse({'message': 'Invalid request'}, status=400)
