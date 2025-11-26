from urllib import request
from django.contrib.auth import authenticate, login,logout
from django.shortcuts import render, redirect
from django.contrib import messages

from accounts.models import CustomUser
from .decorators import allowed_users, unauthenticated_user,require_vendor
from orders.models import Order, OrderItem
from .forms import RegisterForm
from django.contrib.auth.decorators import login_required
from products.models import product
from django.shortcuts import render, get_object_or_404


from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import RegisterForm
from django.contrib.auth.models import Group


@unauthenticated_user
def register_view(request):
    form = RegisterForm()
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user =  form.save()
            username = form.cleaned_data.get('username')
            group = Group.objects.get(name = 'customer')
            user.groups.add(group )
            messages.success(request, f"Account created for {username} successfully! Please login.")
            return redirect('login')
    else:
        form = RegisterForm()

    return render(request, "accounts/register.html", {"form": form})

@unauthenticated_user
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

@login_required(login_url='login')
# @allowed_users(allowed_roles=['vendor'])
# @require_vendor 
def home_view(request):
    return render(request, "accounts/home.html")

@login_required(login_url='login')
def dashboard(request):
    return render(request, "accounts/dashboard.html")

@login_required(login_url='login')
@allowed_users(allowed_roles=['vendor'])
def vendor_dashboard(request):
    products = product.objects.all()
    total_pro = products.count()
    av_pro = product.objects.filter(status='available').count()
    unav_pro = product.objects.filter(status='unavailable').count()
    act_order = Order.objects.filter(status='active')
    paid_order = Order.objects.filter(status='paid')
    pend_order = Order.objects.filter(status='pending').count()
    context = {"products":products,'total':total_pro,"available":av_pro,"pending":pend_order,'unvailable':unav_pro}
    return render(request,'accounts/vendor_dashboard.html',context)

@login_required(login_url='login')
# @allowed_users(allowed_roles=['customer'])
def product_list(request):
    products = product.objects.all()
    return render(request, 'accounts/product_list.html', {'products': products})
@login_required(login_url='login')
def product_detail(request, id):
    prod = get_object_or_404(product, id=id)
    return render(request, 'accounts/product_detail.html', {'product': prod}) 

def userPage():
    return render(request, 'accounts/user.html')
