from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, CartProduct, Cart, Order
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .forms import OrderForm
from dotenv import load_dotenv
import os
import requests
import secrets
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.template.loader import render_to_string

load_dotenv()
secret_key = os.getenv('SECRET_KEY') 

def not_found(request, exception):
    return render(request, '404.html')

def server_error(request):
    return render(request, '500.html')

def check_cookie_support(func):
    def wrapper(request, *args, **kwargs):
        request.session.set_test_cookie()
        if not request.session.test_cookie_worked():
            return HttpResponse('This browser does not support cookies which this website needs to function. Try using another browser or enable cookie support for this one.', status=200)
        else:
            request.session.delete_test_cookie()
            return func(request, *args, **kwargs)
    return wrapper

def home(request):
    products = Product.objects.all()[:4]
    return render(request, 'shop.html', {'products': products})

@check_cookie_support
def checkout(request, order_id):
    order = Order.objects.get(id=order_id)
    if order.active:
        return redirect(f'/trackorder/{order_id}')
    return render(request, 'checkout.html', {'order': order})

@check_cookie_support
def track_order(request, order_id):
    order = Order.objects.get(id=order_id)
    if not order.active:
        return redirect(f'/checkout/{order_id}')
    return render(request, 'trackorder.html', {'order': order})

def check_transaction_status(request, transaction_id):
    url = f"https://api.flutterwave.com/v3/transactions/{transaction_id}/verify"
    headers = {
        "Authorization": f"Bearer {secret_key}"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    return None

def send_verification_email(request, order_id):
    order = Order.objects.get(id=order_id)
    payment_success_mail = EmailMultiAlternatives(
                    'Payment Made Successfully!',
f"""
Hello {order.first_name},

your payment of ₦{order.get_total_price()} was successful and your order ({order.order_id}) has been confirmed.
""",
                    str(settings.DEFAULT_FROM_EMAIL),
                    [str(order.email)],
                    reply_to=['pyjamelnoreply@mail.com']
                )
    html_page = render_to_string('paymentsuccessmail.html', {
        "order": order
    })
    payment_success_mail.attach_alternative(html_page, 'text/html')
    payment_success_mail.send(fail_silently=False)
    return None

def activate_order(request, order_id, transaction_id):
    transaction_id = str(transaction_id)
    order = Order.objects.get(id=order_id)
    if order.active:
        return redirect(f'/trackorder/{order_id}')
    transaction_id_exists_for_order = Order.objects.filter(transaction_id=transaction_id).count() > 0
    if transaction_id_exists_for_order:
        return redirect(f'/checkout/{order_id}/')
    if not transaction_id:
        return HttpResponse('Transaction ID missing!')
    transaction_data = check_transaction_status(request, transaction_id)
    if transaction_data:
        if str(transaction_data['status']).lower() == 'success' and str(transaction_data['data']['status']).lower() == 'successful':
            order.active = True
            order.transaction_id = transaction_id
            order.save()
            email_value = send_verification_email(request, order_id)
            print(email_value)
            return render(request, 'paymentsuccess.html', {'order': order})
        elif str(transaction_data['data']['status']).lower() == 'failed':
            return render(request, 'paymentfailed.html', {'order': order})
        else:
            return render(request, 'paymentprocessing.html', {'order': order})
    return HttpResponse('No transaction data!')

@check_cookie_support
def product_list(request):
    products = Product.objects.all()
    cart_id_exists = request.session.__contains__("cart_id")
    if cart_id_exists:
        cart_id = request.session.__getitem__("cart_id")
        cart = Cart.objects.get(id=cart_id)
        return render(request, 'product_list.html', {'products': products, 'cart': cart})
    return render(request, 'product_list.html', {'products': products})

def get_cart(request):
    cart_id_exists = request.session.__contains__("cart_id")
    if cart_id_exists:
        cart_id = request.session.__getitem__("cart_id")
        print(f'GETTING CART ID: {cart_id}')
        cart = get_object_or_404(Cart, id=int(cart_id))
    else:
        cart = Cart.objects.create()
        request.session.__setitem__("cart_id", cart.id)
        print(f'SETTING CART ID: {cart.id}')
    return cart

@csrf_exempt
@check_cookie_support
def add_to_cart(request, product_id):
    if request.method == 'POST':
        cart = get_cart(request)
        product = get_object_or_404(Product, id=product_id)
        check_cart_product_exists = CartProduct.objects.filter(product=product, cart=cart).count() > 0
        if check_cart_product_exists:
            existing_cart_product = CartProduct.objects.get(product=product, cart=cart)
            existing_cart_product.delete()
            return JsonResponse({'message': f'{product.name} removed from cart!',
                                 'status': 'removed',
                                 'cartItemCount': cart.cartproduct_set.count(),
                                 'cartTotalItems': cart.get_total_items(),
                                 'cartTotalPrice': cart.get_total_price()})
        CartProduct.objects.create(product=product, cart=cart)
        return JsonResponse({'message': f'{product.name} added to cart!',
                             'status': 'added',
                             'cartItemCount': cart.cartproduct_set.count(),
                             'cartTotalItems': cart.get_total_items(),
                             'cartTotalPrice': cart.get_total_price()})

@check_cookie_support
def cart(request):
    cart = get_cart(request)
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save()
            while True:
                order_id = secrets.token_hex(5)
                if Order.objects.filter(order_id=order_id).all().count() == 0:
                    order.order_id = order_id
                    order.save()
                    break
            for cartproduct in cart.cartproduct_set.all():
                order.cartproducts.add(cartproduct)
                cartproduct.cart = None
                cartproduct.save()
            return redirect(f'/checkout/{order.id}/')
        return render(request, "cart.html", {"cart": cart, "form": form})
    form = OrderForm()
    return render(request, "cart.html", {"cart": cart, "form": form})

@csrf_exempt
@check_cookie_support
def increase(request, cartproduct_id):
    if request.method == 'POST':
        cart = get_cart(request)
        cartproduct = get_object_or_404(CartProduct, id=cartproduct_id)
        if cartproduct.cart != cart:
            return HttpResponse(f'Your request has been denied as you do not own cart product {cartproduct_id}')
        cartproduct.quantity = cartproduct.quantity + 1
        cartproduct.save()
        return JsonResponse({'message': f'Added 1 {cartproduct.product.name} to cart!',
                                'status': 'added',
                                'cartProductCount': cartproduct.quantity,
                                'totalPrice': cartproduct.total_price(),
                                'cartTotalItems': cart.get_total_items(),
                                'cartTotalPrice': cart.get_total_price()
                                })

@csrf_exempt
@check_cookie_support
def decrease(request, cartproduct_id):
    if request.method == 'POST':
        cart = get_cart(request)
        cartproduct = get_object_or_404(CartProduct, id=cartproduct_id)
        if cartproduct.cart != cart:
            return HttpResponse(f'Your request has been denied as you do not own cart product {cartproduct_id}')
        cartproduct.quantity = cartproduct.quantity - 1
        cartproduct.save()
        return JsonResponse({'message': f'Removed 1 {cartproduct.product.name} from cart!',
                             'status': 'removed',
                             'cartProductCount': cartproduct.quantity,
                             'totalPrice': cartproduct.total_price(),
                             'cartTotalItems': cart.get_total_items(),
                             'cartTotalPrice': cart.get_total_price()
                             })
