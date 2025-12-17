from .models import Category, Wishlist, Cart
from django.db.models import Sum

def categories(request):
    return {
        'categories': Category.objects.all()
    }

def global_counts(request):
    wishlist_count = 0
    cart_count = 0
    
    if request.user.is_authenticated:
        # Wishlist Count
        wishlist_count = Wishlist.objects.filter(user=request.user).count()
        
        # Cart Count (Sum of quantities)
        try:
            cart = Cart.objects.get(user=request.user)
            # Aggregate returns {'quantity__sum': value}
            result = cart.items.aggregate(Sum('quantity'))
            cart_count = result['quantity__sum'] or 0
        except Cart.DoesNotExist:
            cart_count = 0
            
    return {
        'wishlist_count': wishlist_count,
        'cart_count': cart_count
    }
