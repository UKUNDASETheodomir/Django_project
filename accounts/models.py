from django.db import models
from django.contrib.auth.models import AbstractUser,User
from django.conf import settings
from random import randint



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



class OTPToken(models.Model): 
    Auth_method_CHOICES = [
          ('email', 'Email'),
          ('app', 'authenticator app')
            ]
    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                 on_delete=models.CASCADE,
                                   related_name='otp_email') 
    opt_code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    expired_at = models.DateTimeField() 
    auth_method = models.CharField(max_length=50, choices=Auth_method_CHOICES, default='email') 


    def __str__(self):
        return f"OTP for {self.user.username} via {self.auth_method}"
    
    class Meta:
         ordering = ['-created_at']