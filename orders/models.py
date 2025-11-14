from django.db import models
from django.conf import settings

class Orders(models.Model):
    
    STATUS_CHOICE = [
        ("PENDING","Pending"),
        ("PAID","Paid"),
        ("ACTIVE","Active")
    ]
    
    customer = models.ForeignKey('accounts.User',on_delete = models.CASCADE)
    phone = models.IntegerField()
    delivery_address = models.PositiveBigIntegerField()
    created_at  = models.DateTimeField(auto_now_add=True)
    status_choice = models.CharField(max_length=255,choices = STATUS_CHOICE)
    total = models.IntegerField()

def __str__(self):
   return f"Order #{self.id} - {self.customer.get_full_name()}"
      




class OrderItem(models.Model): 
    order = models.ForeignKey('Order', on_delete = models.CASCADE)
    product = models.ForeignKey('product', on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.IntegerField()
    



