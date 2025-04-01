from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, CartProduct, Cart, Order, Post
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .forms import OrderForm
from dotenv import load_dotenv
import os
import requests
import secrets
from django.core.mail import EmailMultiAlternatives, send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required, permission_required
import json
import random


load_dotenv()
secret_key = os.getenv('SECRET_KEY')


def send_email(request):
    html = render_to_string('emailcode.html')
    send_mail(
        'Email title',
        'Hello world',
        'Mapp <pyjamel224@gmail.com>',
        ['fluxlite224@gmail.com'],
        False,
        'pyjamel224@gmail.com',
        str(os.getenv('EMAIL_HOST_PASSWORD')),
        html
    )
    return 'Email sent success!'


def bet15(request):
    rem = 0
    if not request.session.__contains__('bets'):
        print('No bet session')
        request.session.__setitem__('bets', str(rem))
    else:
        rem = int(request.session.__getitem__('bets'))
        print('REM: ', rem)
    if request.method == 'POST':
        if rem == 0:
            msg = 'Insufficient bets!'
            return render(request, 'bet15home.html', {'msg': msg, 'rem': rem})
        
        res = [random.randint(1, 6) for _ in range(3)]
        request.session.__setitem__('bets', str(rem - 1))
        rem -= 1
        msg = ''
        if res == [6, 6, 6]:
            msg = 'You win!'
        elif res.count(6) == 2:
            msg = 'So close!'
        else:
            msg = 'You lose, try again!'
        
        # def check(dice, faces):
        # res = [random.randint(1, faces) for _ in range(dice)]
        # msg = ''
        # dice = 4
        # count = 0
        # for i in range(1, dice):
        #     if res[0] == res[i]:
        #         count += 1
        # if count == dice - 1:
        #     print(f'Correct: {res}')
        #     msg = 'You win!'
        # elif count == dice - 2:
        #     print(f'So close: {res}')
        #     msg = 'So close!'
        # else:
        #     print(f'Wrong: {res}')
        #     msg = 'You lose, try again!'
        # return count == dice - 1
        return render(request, 'bet15.html', {'res': res, 'msg': msg, 'rem': rem})
    return render(request, 'bet15home.html', {'rem': rem})

def buy15(request):
    rem = int(request.session.__getitem__('bets'))
    request.session.__setitem__('bets', str(rem + 10))
    return redirect('/bet15/')

def get_posts(request):
    print(request.headers)
    posts = Post.objects.all()
    res = HttpResponse(f"{len(posts)} posts")
    return res

def create_post(request):
    print(request.headers)
    if request.method == 'POST':
        data = request.POST
        title = data.get('title')
        content = data.get('content')
        print(title, content)

        if title and content:
            post = Post.objects.create(title=title, content=content)
            print(f'POST WITH ID OF {post.id} CREATED!')
            return redirect('/getposts/')
        
        return HttpResponse('Invalid create post data')

def edit_post(request, id):
    if request.method == 'POST':
        try:
            post = Post.objects.get(id=id)
        except Post.DoesNotExist:
            return HttpResponse('Post does not exist')
        
        print(request.POST)
        data = request.POST
        title = data.get('title')
        content = data.get('content')
        print(title, content)

        if title and content:
            post.title = title
            post.content = content
            post.save()
            return redirect('/getposts/')

        return HttpResponse('Invalid edit post data')

def delete_post(request, id):
    if request.method == 'POST':
        try:
            post = Post.objects.get(id=id)
        except Post.DoesNotExist:
            return HttpResponse('Post does not exist')
        
        post.delete()

        return redirect('/getposts/')
        
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
