from django.urls import path
from django.contrib import admin
from django.urls import path,include
from .views import *

app_name = 'Order'

urlpatterns = [
    # path('checkout/',checkout,name="checkout"), 
    path('checkout/<str:action>',checkout,name="checkout"), 
    path('checkout/<str:action>',checkout,name="changeCheckoutAddrs"), 
    # path('checkout/<int:pid>/',checkout,name="checkout"), 
    
    path('my-orders/',orderHistory,name="orderHistory"), 
    path('track-order/',orderTrack,name="orderTrack"), 
    path('cancel-order/<int:id>/',orderCancel,name="orderCancel"), 
    path('return-order/<int:id>/',orderReturn,name="orderReturn"), 


]
