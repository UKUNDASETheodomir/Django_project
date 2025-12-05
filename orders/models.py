from django.db import models
from django.conf import settings
from products.models import product

class Order(models.Model):
    
    STATUS_CHOICE = [
        ("PENDING","Pending"),
        ("PAID","Paid"),
        ("ACTIVE","Active")
    ]
    
    customer = models.ForeignKey('accounts.CustomUser',on_delete = models.CASCADE)
    phone = models.CharField( max_length=50)
    delivery_address = models.CharField(max_length=255)
    created_at  = models.DateTimeField(auto_now_add=True)
    status= models.CharField(max_length=255,choices = STATUS_CHOICE)
    total = models.IntegerField()

    def __str__(self):
        return f"Order {self.customer.username}"

      




class OrderItem(models.Model): 
    order = models.ForeignKey('Order', on_delete = models.CASCADE)
    product = models.ForeignKey(product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.IntegerField()
    



