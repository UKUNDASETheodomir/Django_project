from django import forms
from .models import product

class ProductForm(forms.ModelForm):
    class Meta:
        model = product
        fields = ['name', 'description', 'price', 'stock', 'image']

        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter product name'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Enter product description',
                'rows': 4,
            }),
            'price': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter price'
            }),
            'stock': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Stock quantity'
            }),
            'image': forms.ClearableFileInput(attrs={
                'class': 'form-control',
            }),
        }

    def clean_image(self):
        image = self.cleaned_data.get('image')

        if image:
            if not image.content_type in ['image/jpeg', 'image/png']:
                raise forms.ValidationError("Only JPEG and PNG images are allowed.")
        return image
