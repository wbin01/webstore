import os
from dotenv import load_dotenv

from django.urls import path

from .views import (
    buy_request,
    cart, cart_request, cart_request_edit, cart_request_remove,
    favorite_request,
    index,
    login, logout,
    product,
    signup,
    search, search_tag)

load_dotenv()
ADMIN_ROUTE = os.getenv('ADMIN_ROUTE')

urlpatterns = [
    path('buy_request/<int:product_id>:<int:quantity>/',
         buy_request, name='buy_request'),
    path('cart/',
         cart, name='cart'),
    path('cart_request/<int:product_id>/',
         cart_request, name='cart_request'),
    path('cart_request_edit/<int:product_id>/',
         cart_request_edit, name='cart_request_edit'),
    path('cart_request_remove/<int:product_id>/',
         cart_request_remove, name='cart_request_remove'),
    path('favorite_request/<int:product_id>/',
         favorite_request, name='favorite_request'),
    path('',
         index, name='index'),
    path('login/',
         login, name='login'),
    path('logout/',
         logout, name='logout'),
    path('product/<str:product_url_title>:<int:product_id>/',
         product, name='product'),
    path('search/',
         search, name='search'),
    path('search_tag/',
         search_tag, name='search_tag'),
    path('signup/',
         signup, name='signup'),
]
