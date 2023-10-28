from django.contrib import admin
from .models import Product, Order


# Register your models here.
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    model = Product
    list_display = ['name', 'description', 'price', 'user']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    model = Order
    list_display = ['customer_email', 'product', 'amount', 'has_paid', 'created_on', 'updated_on']