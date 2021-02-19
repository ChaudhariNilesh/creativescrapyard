from django.urls import path
from django.contrib import admin
from django.urls import path,include
from .views import *

app_name = 'Order'

urlpatterns = [
    # path('checkout/',checkout,name="checkout"), 
    path('checkout/<int:pid>',checkout,name="checkout"), 
    path('checkout/change-address/',checkout,name="changeCheckoutAddrs"), 

    path('my-orders/',orderHistory,name="orderHistory"), 
    path('track-order/',orderTrack,name="orderTrack"), 
]
