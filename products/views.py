from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import ProductForm
from .models import product

@login_required
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


@login_required
def vendor_products(request):
    products = product.objects.filter(vendor=request.user)
    return render(request, "products/vendor_products.html", {"products": products})
def product_list(request):
    # Show only active products
    products = product.objects.filter(status='active')
    return render(request, 'products/product_list.html', {'products': products})
@login_required
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

