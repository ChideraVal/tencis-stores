from django import forms
from .models import Order


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = '__all__'
        exclude = ['order_id', 'transaction_id', 'active', 'shipped', 'processed', 'delivered', 'cartproducts', 'create_time', 'processed_time', 'shipped_time', 'delivered_time']
    