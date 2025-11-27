from django.contrib import admin
from .models import*


class Adminorder(admin.ModelAdmin):
    display_list = (' total', 'status', 'created_at')
    search_list = ('name')
    list_filter = ('status', 'created_at')
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'total', 'status', 'created_at')
    list_filter = ('status',)
    search_fields = ('customer__username',)

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'order', 'product', 'quantity', 'price')
    list_filter = ('order', 'product')
