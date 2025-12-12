from urllib import request
from django.contrib.auth import authenticate, login,logout
from django.shortcuts import render, redirect
from django.contrib import messages

from accounts.models import CustomUser
from .decorators import  vendor_required, customer_required
from orders.models import Order, OrderItem
from .forms import RegisterForm
from django.contrib.auth.decorators import login_required
from products.models import product
from django.shortcuts import render, get_object_or_404


from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import RegisterForm
from django.contrib.auth.models import Group


def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)

            user_type = form.cleaned_data.get('user_type')
            user.user_type = user_type
            user.save()

            if user_type == 'C':
                group = Group.objects.get(name='customer')
            else:
                group = Group.objects.get(name='vendor')

            user.groups.add(group)

            messages.success(request, f"Account created successfully")
            login(request, user)
            return redirect("dashboard")
    else:
        form = RegisterForm()

    return render(request, "accounts/register.html", {"form": form})


def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("dashboard")  
        else:
            messages.info(request, "Invalid username or password")
    
    context = {}
    return render(request, "accounts/login.html",context)

def logout_view(request):
    logout(request)
    return redirect("login")

def home_view(request):
    products= product.objects.all()
    return render(request, "accounts/home.html",{'products':products})

# @allowed_users(allowed_roles=['vendor'])
@login_required(login_url='login')
def dashboard(request):
    return render(request, "accounts/dashboard.html")


@vendor_required
def vendor_dashboard(request):
    # Get all products for the current vendor
    vendor_products = product.objects.filter(vendor=request.user)

    # Order them by the 'created_at' field to get the most recent ones first
    recent_products = vendor_products.order_by('-created_at')

    # Calculate statistics based only on the vendor's products
    total_pro = vendor_products.count()
    unav_pro = vendor_products.filter(status='unavailable').count()
    
    # TODO: Filter orders based on the vendor's products for accurate stats
    act_order = Order.objects.filter(status='active').count()
    pend_order = Order.objects.filter(status='pending').count()

    context = {"products": recent_products, 'total_pro': total_pro, "act_order": act_order, "pend_order": pend_order, 'unav_pro': unav_pro}
    return render(request,'accounts/vendor_dashboard.html',context)

@login_required(login_url='login')
def product_list(request):
    products = product.objects.all()
    return render(request, 'accounts/product_list.html', {'products': products})
@login_required(login_url='login')
def product_detail(request, id):
    prod = get_object_or_404(product, id=id)
    return render(request, 'accounts/product_detail.html', {'product': prod}) 

@login_required(login_url='login')
# @allowed_users(allowed_roles=['customer'])
def userPage(request):
    return render(request, 'accounts/user.html')


# def HomePage(request):
#     return render(request, 'accounts/home_page.html')
