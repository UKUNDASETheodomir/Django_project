from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from accounts.decorators import vendor_required, customer_required  
from .forms import ProductForm
from .models import Category, product, ProductImage, Wishlist, Cart, CartItem
from django.db.models import Sum, F, DecimalField
from django.contrib import messages
from django.contrib.auth.decorators import login_required


from accounts.decorators import vendor_required, customer_required  
from .forms import ProductForm
from .models import *
from django.db.models import Sum, F, DecimalField


@login_required(login_url='login')
@vendor_required
def vendor_products(request):
    products = product.objects.filter(vendor = request.user)
    context = {"products": products}
    return render(request, "products/vendor_products.html",context)

# @login_required(login_url='login')

def product_list(request):
    products = product.objects.filter(status='available')
    
    # Filter by Category
    category_id = request.GET.get('category')
    if category_id:
        products = products.filter(category_id=category_id)
        
    # Filter by Search Query
    query = request.GET.get('q')
    if query:
        products = products.filter(name__icontains=query)

    # Filter by Price
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    if min_price:
        products = products.filter(price__gte=min_price)
    if max_price:
        products = products.filter(price__lte=max_price)

    context = {
        'products': products,
        'selected_category': int(category_id) if category_id else None,
        'query': query,
    }
    return render(request, 'products/product_list.html', context)


@login_required(login_url='login')
def product_detail(request, id):
    prod = get_object_or_404(product, id=id)
    images = prod.images.all() # Fetch related gallery images
    return render(request, 'accounts/product_detail.html', {'product': prod, 'images': images})
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

            # Handle optional gallery images
            images = [
                request.FILES.get('image1'),
                request.FILES.get('image2'),
                request.FILES.get('image3')
            ]

            for img in images:
                if img:
                    ProductImage.objects.create(product=new_product, image=img)
            
            return redirect('vendor_products')
    else:
        form = ProductForm()

    return render(request, 'products/create_product.html', {'form': form})

@login_required(login_url='login')
@vendor_required
def edit_product(request, id):
    item = get_object_or_404(product, id=id, vendor=request.user)
    
    # Get existing gallery images ordered by ID
    gallery_images = item.images.all().order_by('id')

    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES, instance=item)
        if form.is_valid():
            form.save()
            
            # Handle extra gallery images update
            # Logic: If image1/2/3 is in request.FILES, update or create
            for i in range(1, 4):
                image_field = f'image{i}'
                new_image = request.FILES.get(image_field) # Use request.FILES since form.cleaned_data might require clean_* methods or field definition alignment
                if not new_image and image_field in form.cleaned_data:
                     # Check cleaned data as fallback if defined in form
                     new_image = form.cleaned_data.get(image_field)

                if new_image:
                    # Update existing slot or create new
                    # Since existing images are ordered by ID, we map index 0 -> image1, 1 -> image2, 2 -> image3
                    try:
                        if i <= len(gallery_images):
                            existing_img = gallery_images[i-1]
                            existing_img.image = new_image
                            existing_img.save()
                        else:
                            ProductImage.objects.create(product=item, image=new_image)
                    except IndexError:
                         ProductImage.objects.create(product=item, image=new_image)

            messages.success(request, "Product updated successfully!")
            return redirect('vendor_products')
    else:
        # Pre-populate proper slots
        initial_data = {}
        for idx, img_obj in enumerate(gallery_images):
            if idx < 3:
                initial_data[f'image{idx+1}'] = img_obj.image
        
        form = ProductForm(instance=item, initial=initial_data)

    return render(request, 'products/edit_product.html', {'form': form, 'product': item})

@login_required(login_url='login')
@vendor_required
def delete_product(request, id):
    item = get_object_or_404(product, id=id, vendor=request.user)

    if request.method == "POST":  # confirm delete
        item.delete()
        messages.success(request, "Product deleted successfully!")
        return redirect('vendor_products')

    return render(request, 'products/delete_product_confirm.html', {'product': item})


@login_required(login_url='login')
def wishlist_view(request):
    """Displays the user's wishlist."""
    # Fetch all wishlist items for the logged-in user, optimizing the query
    wishlist_items = Wishlist.objects.filter(user=request.user).select_related('product')
    
    context = {
        'items': wishlist_items,
    }
    return render(request, 'accounts/wishlist.html', context)


@login_required(login_url='login')
def add_to_wishlist(request, product_id):
    
    # FIX: Use the model name exactly as defined (lowercase 'product')
    # If the object is not found, get_object_or_404 handles it.
    # The variable assigned is named 'p' to avoid confusion with the model class 'product'.
    p = get_object_or_404(product, id=product_id)
    
    # -------------------------------------------------------------
    # Now, the 'p' variable is guaranteed to exist below this line.
    # -------------------------------------------------------------
    
    # Check if the Wishlist entry already exists for this user/product
    # Use the assigned variable 'p' in the filter
    wishlist_entry = Wishlist.objects.filter(user=request.user, product=p)

    if wishlist_entry.exists():
        # Item exists, so remove it (toggle feature)
        wishlist_entry.delete()
        # Optional: Add success message: "Item removed from wishlist"
    else:
        # Item does not exist, so add it
        Wishlist.objects.create(user=request.user, product=p)
        # Optional: Add success message: "Item added to wishlist"
        
    # Redirect back to the previous page (like the product list or detail page)
    return redirect(request.META.get('HTTP_REFERER', 'home'))


@login_required(login_url='login')
def remove_from_wishlist(request, product_id):
    """Removes a product from the user's wishlist."""
    prod = get_object_or_404(product, id=product_id)
    
    # Delete the specific item for the user
    Wishlist.objects.filter(user=request.user, product=prod).delete()
    
    messages.info(request, f"'{prod.name}' removed from your wishlist.")
    
    # Redirect back to the wishlist page
    return redirect('wishlist')

@login_required(login_url='login')
def cart_view(request):
    """Displays the user's shopping cart."""
    cart, created = Cart.objects.get_or_create(user=request.user)
    
    cart_items = CartItem.objects.filter(cart=cart).select_related('product')
    
    # --- CORRECTED AGGREGATION LOGIC ---
    # 1. Use F() expressions to correctly calculate (quantity * price) for each item
    # 2. Use output_field to ensure the result is treated as a Decimal/Float
    cart_total_result = cart_items.aggregate(
        total_price=Sum(F('quantity') * F('product__price'), 
                        output_field=DecimalField())
    )
    
    # Extract the result, defaulting to 0 if the cart is empty
    cart_total = cart_total_result['total_price'] or 0
    # --- END CORRECTED LOGIC ---

    context = {
        'cart_items': cart_items,
        'cart_total': cart_total,
    }
    return render(request, 'accounts/cart.html', context)

@login_required(login_url='login')
def add_to_cart(request, product_id):
    # 1. Get the product and the user's cart
    p = get_object_or_404(product, id=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    
    # We default the quantity to 1 for a direct "Add" button click
    quantity_to_add = 1 
    
    # 2. Check if the CartItem already exists
    cart_item, item_created = CartItem.objects.get_or_create(
        cart=cart, 
        product=p,
        # Default values if item_created is True
        defaults={'quantity': quantity_to_add} 
    )

    if not item_created:
        # 3. If the item exists, increment the quantity
        cart_item.quantity += quantity_to_add
        cart_item.save()
        # Optional: Add success message "Quantity updated in cart"
    # else:
        # Optional: Add success message "Item added to cart"
        
    # Redirect back to the previous page
    return redirect(request.META.get('HTTP_REFERER', 'home'))


@login_required(login_url='login')
def update_cart_quantity(request, item_id):
    """Updates the quantity of a specific cart item."""
    if request.method == 'POST':
        new_quantity = int(request.POST.get('quantity'))
        cart = get_object_or_404(Cart, user=request.user)
        item = get_object_or_404(CartItem, id=item_id, cart=cart)
        
        if new_quantity > 0:
            item.quantity = new_quantity
            item.save()
            messages.success(request, f"Quantity for '{item.product.name}' updated.")
        else:
            item.delete()
            messages.info(request, f"Removed '{item.product.name}' from cart.")
            
    return redirect('cart')


@login_required(login_url='login')
def remove_from_cart(request, item_id):
    """Removes a specific cart item entirely."""
    cart = get_object_or_404(Cart, user=request.user)
    item = get_object_or_404(CartItem, id=item_id, cart=cart)
    
    item.delete()
    messages.info(request, f"Removed '{item.product.name}' from cart.")
    return redirect('cart')

