from django.urls import path
from . import views

urlpatterns = [
    path('bet15/', views.bet15),
    path('buy15/', views.buy15),
    path('sendemail/', views.send_email),
    path('getposts/', views.get_posts),
    path('createpost/', views.create_post),
    path('editpost/<int:id>/', views.edit_post),
    path('deletepost/<int:id>/', views.delete_post),
    path('', views.home),
    path('products/', views.product_list),
    path('add-to-cart/<int:product_id>/', views.add_to_cart),
    path('cart/', views.cart),
    path('increase/<int:cartproduct_id>/', views.increase),
    path('decrease/<int:cartproduct_id>/', views.decrease),
    path('checkout/<int:order_id>/', views.checkout),
    path('verify/<int:order_id>/<int:transaction_id>/', views.activate_order),
    path('trackorder/<int:order_id>/', views.track_order)
]
