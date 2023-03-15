import os
from dotenv import load_dotenv

from django.urls import path

from .views import *

load_dotenv()
ADMIN_ROUTE = os.getenv('ADMIN_ROUTE')

urlpatterns = [
    path('cart/',
         cart, name='cart'),
    path('favorite/',
         favorite, name='favorite'),
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
    path('manage/store/',
         manage_store, name='manage_store'),
    path('manage/users/',
         manage_users, name='manage_users'),
    path('manage/users/edit/'
         '<str:user_username>/<int:user_profile_id>/',
         manage_users_edit, name='manage_users_edit'),
    path('manage/users/new/',
         manage_users_new, name='manage_users_new'),
    path('product/<str:product_url_title>:<int:product_id>/',
         product, name='product'),
    path('search/',
         search, name='search'),
    path('search_tag/',
         search_tag, name='search_tag'),
    path('signup/',
         signup, name='signup'),
    path('<str:username>/',
         user_dashboard, name='user_dashboard'),
]
