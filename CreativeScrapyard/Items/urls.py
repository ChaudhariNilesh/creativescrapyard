from django.urls import path
from django.contrib import admin
from django.urls import path,include
from .views import *

app_name = 'Items'

urlpatterns = [
    path('single-item/',singleItem,name="Items"), 
    path('cart/',viewCartItem,name="cart"), 
]
