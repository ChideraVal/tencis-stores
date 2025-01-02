from django.template import Library
from shopapp.models import Product, Cart, CartProduct

register = Library()

@register.filter(name='checkincart')
def checkincart(cart, product):
    return cart.cartproduct_set.filter(product=product).count() > 0
