import os
from dotenv import load_dotenv

from django.urls import path

from .views import (
    index, signup, login, logout, product, search, search_tag, buy, cart)

load_dotenv()
ADMIN_ROUTE = os.getenv('ADMIN_ROUTE')

urlpatterns = [
    path('buy/<int:post_id>/', buy, name='buy'),
    path('cart/<int:post_id>/', cart, name='cart'),
    path('', index, name='index'),
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
    path('product/<str:url_title>:<int:post_id>/', product, name='product'),
    path('search/', search, name='search'),
    path('search_tag/', search_tag, name='search_tag'),
    path('signup/', signup, name='signup'),
]
