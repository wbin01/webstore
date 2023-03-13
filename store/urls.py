import os
from dotenv import load_dotenv

from django.urls import path

from .views import *

load_dotenv()
ADMIN_ROUTE = os.getenv('ADMIN_ROUTE')

urlpatterns = [
    path('buy/<int:product_id>/',
         buy, name='buy'),
    path('cart/',
         cart, name='cart'),
    path('cart_edit/<int:cart_id>/',
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
    path('manage/products/',
         manage_products, name='manage_products'),
    path('manage/products/new/',
         manage_products_new, name='manage_products_new'),
    path('manage/products/edit/<str:product_url_title>:<int:product_id>/',
         manage_products_edit, name='manage_products_edit'),
    path('manage/products/edit/save/<int:product_id>/',
         manage_products_edit_save, name='manage_products_edit_save'),
    path('manage/store/',
         manage_store, name='manage_store'),
    path('manage/store/save/',
         manage_store_save, name='manage_store_save'),
    path('manage/users/',
         manage_users, name='manage_users'),
    path('manage/users/edit/'
         '<str:user_username>/<int:user_profile_id>/<str:status>/',
         manage_users_edit, name='manage_users_edit'),
    path('manage/users/edit/save/<int:edit_user_profile_id>/',
         manage_users_edit_save, name='manage_users_edit_save'),
    path('manage/users/new/',
         manage_users_new, name='manage_users_new'),
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
