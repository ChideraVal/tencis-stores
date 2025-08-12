from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('products/', views.product_list, name='product_list'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart, name='view_cart'),
    path('increase/<int:cartproduct_id>/', views.increase, name='increase_quantity'),
    path('decrease/<int:cartproduct_id>/', views.decrease, name='decrease_quantity'),
    path('checkout/<int:order_id>/', views.checkout, name='go_to_checkout'),
    path('verify/<int:order_id>/<int:transaction_id>/', views.activate_order, name='activate_order'),
    path('trackorder/<int:order_id>/', views.track_order, name='track_order')
]