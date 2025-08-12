from django.template import Library

register = Library()

@register.filter(name='checkincart')
def checkincart(cart, product):
    return cart.cartproduct_set.filter(product=product).exists()
