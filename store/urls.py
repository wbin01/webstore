import os
from dotenv import load_dotenv

from django.urls import path

from .views import (
    buy_request,
    cart, cart_edit, cart_remove, cart_favorite,
    favorite, favorite_remove,
    index,
    login, logout,
    manage_products, manage_products_new,
    manage_products_edit, manage_products_edit_save,
    product, product_cart, product_favorite,
    signup,
    search, search_tag)

load_dotenv()
ADMIN_ROUTE = os.getenv('ADMIN_ROUTE')

urlpatterns = [
    path('buy_request/<int:product_id>:<int:quantity>/',
         buy_request, name='buy_request'),
    path('cart/',
         cart, name='cart'),
    path('cart_edit/<int:product_id>/',
         cart_edit, name='cart_edit'),
    path('cart_remove/<int:product_id>/',
         cart_remove, name='cart_remove'),
    path('cart_favorite/<int:product_id>/',
         cart_favorite, name='cart_favorite'),
    path('favorite/',
         favorite, name='favorite'),
    path('favorite_remove/<int:product_id>/',
         favorite_remove, name='favorite_remove'),
    path('',
         index, name='index'),
    path('login/',
         login, name='login'),
    path('logout/',
         logout, name='logout'),
    path('manage/products/new/',
         manage_products_new, name='manage_products_new'),
    path('manage/products/edit/<str:product_url_title>:<int:product_id>/',
         manage_products_edit, name='manage_products_edit'),
    path('manage/products/edit/save/<int:product_id>/',
         manage_products_edit_save, name='manage_products_edit_save'),
    path('manage/products/',
         manage_products, name='manage_products'),
    path('product/<str:product_url_title>:<int:product_id>/',
         product, name='product'),
    path('product_cart/<int:product_id>/',
         product_cart, name='product_cart'),
    path('product_favorite/<int:product_id>/',
         product_favorite, name='product_favorite'),
    path('search/',
         search, name='search'),
    path('search_tag/',
         search_tag, name='search_tag'),
    path('signup/',
         signup, name='signup'),
]
