from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):

    USER_CHOICE_CUSTOMER= 'C',
    USER_CHOICE_VENDOR= 'V',

    USER_CHOICE = [
        ('V','Vendor'),
        ('C','Customer'),
       
    ]
    phone = models.CharField(max_length=15, blank=True, null=True)
    location = models.CharField(max_length=255)
    user_type= models.CharField(max_length = 150,choices= USER_CHOICE, default= USER_CHOICE_CUSTOMER)
 
def __str__(self):
        return self.username

