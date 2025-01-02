from django.contrib import admin
from .models import *


class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price']


class CartAdmin(admin.ModelAdmin):
    list_display = ['id']


class CartProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'quantity']


class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_id', 'email', 'active']

admin.site.register(Product, ProductAdmin)
admin.site.register(Cart, CartAdmin)
admin.site.register(CartProduct, CartProductAdmin)
admin.site.register(Order, OrderAdmin)

