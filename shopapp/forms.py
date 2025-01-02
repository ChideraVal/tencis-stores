from django import forms
from .models import Order


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        exclude = ['order_id', 'transaction_id', 'active', 'shipped', 'processed', 'delivered', 'cartproducts', 'create_time', 'processed_time', 'shipped_time', 'delivered_time']
    
    def clean_phone(self):
        phone_number = self.cleaned_data['phone']
        if not phone_number.isnumeric():
            raise forms.ValidationError('Phone number should be entirely numeric.')
        return phone_number
