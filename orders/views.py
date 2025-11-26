from django.shortcuts import render
from .models import*
# Create your views here.
def vendorOrder(request):
    orders = Order.objects.all()
    ordersitems = OrderItem.objects.all()
    context = {"orders":orders,"items":ordersitems}
    return render(request, "vend_order.html", context)