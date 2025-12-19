from django import forms
from .models import product

class ProductForm(forms.ModelForm):
    class Meta:
        model = product
        fields = ['name', 'description', 'price', 'unit', 'stock', 'category', 'image']

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
            'unit': forms.Select(attrs={
                'class': 'form-select', 
            }),
            'category': forms.Select(attrs={
                'class': 'form-select',
            }),
            'image': forms.ClearableFileInput(attrs={
                'class': 'form-control',
            }),
        }

    def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.fields['image'].required = False

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

from .models import Review

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']
        widgets = {
            'rating': forms.NumberInput(attrs={
                'class': 'form-control', 
                'min': '1', 
                'max': '5',
                'placeholder': 'Rate 1-5'
            }),
            'comment': forms.Textarea(attrs={
                'class': 'form-control', 
                'rows': 3,
                'placeholder': 'Write your review here...'
            }),
        }
