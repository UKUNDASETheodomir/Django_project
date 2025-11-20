from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from .models import CustomUser

User = get_user_model()

class RegisterForm(UserCreationForm):
    USER_TYPE_CHOICES = (
        ('C', 'Customer'),
        ('V', 'Vendor'),
      )
    
    
    user_type = forms.ChoiceField(
        choices=USER_TYPE_CHOICES,       
        widget=forms.Select(attrs={      
            'class': 'form-select',     
        }),
        required=True                   
    )
    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Enter your password',
            'class': 'form-control',
        })
    )

    
    password2 = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Confirm your password',
            'class': 'form-control',
        })
    )
    
    class Meta:
        model = User               # The custom user model to save data
        fields = ['username', 'email', 'user_type', 'password1', 'password2']  # Fields to include in the form
        
        widgets = {
            'username': forms.TextInput(attrs={
                'placeholder': 'Enter your username',
                'class': 'form-control',     # Bootstrap class for styling
            }),
            'email': forms.EmailInput(attrs={
                'placeholder': 'Enter your email',
                'class': 'form-control',
            }),
          
        }