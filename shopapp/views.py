from dotenv import load_dotenv
import os
import requests
from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, CartProduct, Cart, Order
from django.core.mail import send_mail
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .forms import OrderForm
import secrets

load_dotenv()

secret_key = os.getenv('SECRET_KEY') 

def home(request):
    products = Product.objects.all()[:4]
    return render(request, 'shop.html', {'products': products})

def checkout(request, order_id):
    order = Order.objects.get(id=order_id)
    return render(request, 'checkout.html', {'order': order})

def check_transaction_status(request, transaction_id):
    url = f"https://api.flutterwave.com/v3/transactions/{transaction_id}/verify"
    headers = {
        "Authorization": f"Bearer {secret_key}"
    }
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        return response.json()
    return None

def activate_order(request, order_id, transaction_id):
    transaction_id = str(transaction_id)
    
    if not transaction_id:
        return HttpResponse('Transaction ID missing!')

    transaction_data = check_transaction_status(request, transaction_id)

    if transaction_data:
        if str(transaction_data['status']).lower() == 'success' and str(transaction_data['data']['status']).lower() == 'successful':
            order = Order.objects.get(id=order_id)
            order.active = True
            order.transaction_id = transaction_id
            order.save()
            return render(request, 'paymentsuccess.html', {'order': order})

        elif str(transaction_data['data']['status']).lower() == 'failed':
            return render(request, 'paymentfailed.html', {'order': order})
        else:
            return render(request, 'paymentprocessing.html', {'order': order})
    return HttpResponse('No transaction data!')

def check_cookie_support(request):
    request.session.set_test_cookie()
    if request.session.test_cookie_worked():
        return HttpResponse("This browser doesn't support cookies, please try using another browser that supports cookies.")
    request.session.delete_test_cookie()
    return None

@csrf_exempt
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
def add_to_cart(request, product_id):
    if request.method == 'POST':
        cart = get_cart(request)
        product = get_object_or_404(Product, id=product_id)
        check_cart_product_exists = CartProduct.objects.filter(product=product, cart=cart).count() > 0
        if check_cart_product_exists:
            print('IT EXISTS!!!')
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
                    print(f'ORDER ID: {order_id}')
                    break
            for cartproduct in cart.cartproduct_set.all():
                order.cartproducts.add(cartproduct)
                cartproduct.cart = None
                cartproduct.save()
            return redirect(f'/checkout/{order.id}/')
        print(form.errors)
        return render(request, "cart.html", {"cart": cart, "form": form})
    form = OrderForm()
    return render(request, "cart.html", {"cart": cart, "form": form})

@csrf_exempt
def increase(request, cartproduct_id):
    if request.method == 'POST':
        cart = get_cart(request)
        cartproduct = get_object_or_404(CartProduct, id=cartproduct_id)
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
def decrease(request, cartproduct_id):
    if request.method == 'POST':
        cart = get_cart(request)
        cartproduct = get_object_or_404(CartProduct, id=cartproduct_id)
        cartproduct.quantity = cartproduct.quantity - 1
        cartproduct.save()
        
        return JsonResponse({'message': f'Removed 1 {cartproduct.product.name} from cart!',
                             'status': 'removed',
                             'cartProductCount': cartproduct.quantity,
                             'totalPrice': cartproduct.total_price(),
                             'cartTotalItems': cart.get_total_items(),
                             'cartTotalPrice': cart.get_total_price()
                             })
