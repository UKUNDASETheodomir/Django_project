from django.shortcuts import render, get_object_or_404, redirect
from .form import OrderForm
from .models import Order, OrderItem
from products.models import product

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
            if product_obj.stock >= quantity:
                product_obj.stock -= quantity
                product_obj.save()

            return redirect("order_confirmation", id=order.id)
  

    else:
        form = OrderForm()

    return render(request, "orders/place_order.html", {
        "form": form,
        "product": product_obj
    })
def order_confirmation(request, id):
    
    order = get_object_or_404(Order, id=id, customer=request.user)
    order_items = OrderItem.objects.filter(order=order)
    for item in order_items:
        item.line_total = item.quantity * item.price

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
def vendor_orders(request):
    vendor = request.user  # assuming vendor is logged in

    # get all order items that belong to this vendor's products
    order_items = OrderItem.objects.filter(product__vendor=vendor)

    # get distinct orders from these items
    orders = Order.objects.filter(orderitem__in=order_items).distinct()
    
    orders_with_totals = []
    for order in orders:
        total = 0
        vendor_items = []
        for item in order.orderitem_set.all():
            if item.product.vendor == vendor:
                total += item.price
                vendor_items.append(item)
        orders_with_totals.append({
            "order": order,
            "items": vendor_items,
            "total": total
        })

    context = {
        "orders": orders,
        "vendor": vendor,
         "orders_with_totals": orders_with_totals
    }
    return render(request, "orders/vendor_orders.html", context)
