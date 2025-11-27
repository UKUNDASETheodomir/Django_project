from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required


from accounts.decorators import vendor_required, customer_required  
from .forms import ProductForm
from .models import product

@login_required(login_url='login')
def create_product(request):
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.vendor = request.user   # auto-assign vendor
            product.save()
            messages.success(request, "Product created successfully!")
            return redirect("vendor_products")
    else:
        form = ProductForm()

    return render(request, "products/create_product.html", {"form": form})


@login_required(login_url='login')
@vendor_required
def vendor_products(request):
    products = product.objects.filter(vendor = request.user)
    context = {"products": products}
    return render(request, "products/vendor_products.html",context)

# @login_required(login_url='login')

def product_list(request,id):
    products = product.objects.filter(status='active')
    return render(request, 'products/product_list.html', {'products': products})
@login_required(login_url='login')
def create_product(request):
    if request.user.user_type != 'V':
        return redirect('home')
    
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            new_product = form.save(commit=False)
            new_product.vendor = request.user
            new_product.save()
            return redirect('vendor_products')
    else:
        form = ProductForm()

    return render(request, 'products/create_product.html', {'form': form})

