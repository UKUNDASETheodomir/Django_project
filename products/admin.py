from django.contrib import admin
from .models import product

@admin.register(product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'vendor', 'price', 'stock', 'status')
    list_filter = ('status', 'vendor')
    search_fields = ('name', 'vendor__username')
