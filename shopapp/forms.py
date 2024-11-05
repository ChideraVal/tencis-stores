from django import forms
from .models import Order


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = '__all__'
        exclude = ['order_id', 'transaction_id', 'active', 'cartproducts', 'create_time']
    