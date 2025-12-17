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

    # Extra fields for multiple images (not part of the model directly)
    image1 = forms.ImageField(required=False, widget=forms.ClearableFileInput(attrs={'class': 'form-control', 'accept': 'image/*'}))
    image2 = forms.ImageField(required=False, widget=forms.ClearableFileInput(attrs={'class': 'form-control', 'accept': 'image/*'}))
    image3 = forms.ImageField(required=False, widget=forms.ClearableFileInput(attrs={'class': 'form-control', 'accept': 'image/*'}))

    def clean_image(self):
        image = self.cleaned_data.get('image')

        if image:
            if not image.content_type in ['image/jpeg', 'image/png']:
                raise forms.ValidationError("Only JPEG and PNG images are allowed.")
        return image
