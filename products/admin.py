from django.contrib import admin
from .models import product, Category

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    prepopulated_fields = {'slug': ('name',)}

@admin.register(product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'vendor', 'price', 'stock', 'status')
    list_filter = ('status', 'vendor')
    search_fields = ('name', 'vendor__username')
