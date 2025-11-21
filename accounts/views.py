from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import RegisterForm
from django.contrib.auth.decorators import login_required
from products.models import product
from django.shortcuts import render, get_object_or_404


def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user=form.save()
            login(request, user)
            messages.success(request, "Account created successfully!")
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
            return redirect("dashboard")  # change to your homepage
        else:
            messages.error(request, "Invalid username or password")

    return render(request, "accounts/login.html")

def logout_view(request):
    logout(request)
    return redirect("login")

def home_view(request):
    return render(request, "accounts/home.html")
@login_required
def dashboard(request):
    return render(request, "accounts/dashboard.html")

@login_required
def vendor_dashboard(request):
    return render(request, 'accounts/vendor_dashboard.html')
@login_required
def product_list(request):
    products = product.objects.all()
    return render(request, 'accounts/product_list.html', {'products': products})
@login_required
def product_detail(request, id):
    prod = get_object_or_404(product, id=id)
    return render(request, 'accounts/product_detail.html', {'product': prod})