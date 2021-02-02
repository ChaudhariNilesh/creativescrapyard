from django.urls import path
from django.contrib import admin
from django.urls import path,include
from .views import *

app_name = 'Items'

urlpatterns = [
    path('creative-single-item/',creativeSingleItem,name="creativeSingleItem"), 
    path('scrap-single-item/',scrapSingleItem,name="scrapSingleItem"), 
    path('cart/',include('Cart.urls')), 
    path('order/',include('Order.urls')),

    ]
