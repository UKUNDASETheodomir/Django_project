from django.db import models
from django.conf import settings

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=50)
    image = models.ImageField(upload_to='media/categories/', null=True, blank=True)
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name

class product(models.Model):
    
    STATUS_CHOICES = (
        ('available', 'Available'),
        ('unavailable', 'Unavailable'),
    )
    
    UNIT_CHOICES = (
        ('kg', 'Kilogram (kg)'),
        ('g', 'Gram (g)'),
        ('lb', 'Pound (lb)'),
        ('bag', 'Bag'),
        ('box', 'Box'),
        ('liter', 'Liter (L)'),
        ('ml', 'Milliliter (ml)'),
        ('pc', 'Piece (pc)'),
        ('dozen', 'Dozen'),
        ('pack', 'Pack'),
        ('meter', 'Meter (m)'),
    )

    vendor = models.ForeignKey('accounts.CustomUser',on_delete = models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=15)
    description = models.TextField()
    price = models.DecimalField(max_digits=20,decimal_places=4)
    stock = models.IntegerField()
    image = models.ImageField(upload_to='media/products/')
    unit = models.CharField(max_length=50, choices=UNIT_CHOICES, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='available')
    
    
    def __str__(self):
        return self.name 

    def get_average_rating(self):
        reviews = self.reviews.all()
        if reviews.exists():
            return reviews.aggregate(models.Avg('rating'))['rating__avg'] or 0
        return 0
    
    
class Wishlist(models.Model):
    """Links a CustomUser to a product they wishlisted."""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='wishlist_items')
    product = models.ForeignKey('product', on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'product')
        ordering = ['-added_at']

    def __str__(self):
        return f"{self.user.username}'s wishlist: {self.product.name}"

class Cart(models.Model):
    """The shopping cart itself, linked to the user."""
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='cart')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Cart for {self.user.username}"

class CartItem(models.Model):
    """Items inside the shopping cart."""
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey('product', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        unique_together = ('cart', 'product')

    def line_total(self):
        # Calculates the total price for this item (e.g., 3 x $5.00)
        return self.quantity * self.product.price

    def __str__(self):
        return f"{self.quantity} x {self.product.name} in {self.cart.user.username}'s Cart"


class ProductImage(models.Model):
    """Additional images for a product gallery."""
    product = models.ForeignKey(product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='media/products/gallery/')
    
    def __str__(self):
        return f"Image for {self.product.name}"

class Review(models.Model):
    """Product reviews and ratings by customers."""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product = models.ForeignKey(product, on_delete=models.CASCADE, related_name='reviews')
    rating = models.IntegerField(default=5, help_text="Rating from 1 to 5")
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} - {self.product.name} ({self.rating})"