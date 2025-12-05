from django import forms
from .models import Order

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['phone', 'delivery_address']

        widgets = {
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter phone number',
            }),
            'delivery_address': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter delivery address',
            }),
        }
