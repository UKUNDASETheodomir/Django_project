from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

User = get_user_model()

class RegisterForm(UserCreationForm):
    # Override password fields here, outside Meta
      
    username = forms.CharField(
        label="username",
        widget=forms.TextInput(attrs={
            'placeholder': 'Enter your username',
            'class': 'form-control',
        })
    )
    location = forms.CharField(
        label="location",
        widget=forms.TextInput(attrs={
            'placeholder': 'Enter your location',
            'class': 'form-control',
        })
    )
    phone = forms.CharField(
        label="phone",
        widget=forms.TextInput(attrs={
            'placeholder': 'Enter your phone',
            'class': 'form-control',
        })
    )
    email = forms.CharField(
        label="email",
        widget=forms.TextInput(attrs={
            'placeholder': 'Enter your email',
            'class': 'form-control',
        })
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
        model = User
        fields = ['username', 'email', 'user_type', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={
                'placeholder': 'Enter your username',
                'class': 'form-control',
            }),
            'email': forms.EmailInput(attrs={
                'placeholder': 'Enter your email',
                'class': 'form-control',
            }),
            'user_type': forms.Select(attrs={
                'class': 'form-control',
            })
        }
