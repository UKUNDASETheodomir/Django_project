from django.db import models

# Create your models here.
class product(models.Model):
    
    STATUS_CHOICES = (
        ('available', 'Available'),
        ('unavailable', 'Unvailable'),
    )
    vendor = models.ForeignKey('accounts.CustomUser',on_delete = models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=20,decimal_places=4)
    stock = models.IntegerField()
    image = models.ImageField(upload_to='media/products/')
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='available')
    
    
    def __str__(self):
        return self.name