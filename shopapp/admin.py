from django.contrib import admin
from .models import *


class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price']
    list_per_page = 6


class CartProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'quantity']
    list_filter = ['cart']


class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_id', 'email', 'active']


admin.site.site_header = 'Admin Dashboard'
admin.site.site_title = 'Admin Dashboard'

admin.site.register(Product, ProductAdmin)
admin.site.register(Cart)
admin.site.register(CartProduct, CartProductAdmin)
admin.site.register(Order, OrderAdmin)

