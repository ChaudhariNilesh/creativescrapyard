from django.urls import path
from django.contrib import admin
from django.urls import path,include
from .views import *

app_name = 'Items'

urlpatterns = [
    path('creative-single-item/',creativeSingleItem,name="creativeSingleItem"), 
    path('creative-single-item/<int:id>/',creativeSingleItem,name="creativeSingleItem"), 
    path('scrap-single-item/',scrapSingleItem,name="scrapSingleItem"), 
    path('scrap-single-item/<int:id>/',scrapSingleItem,name="scrapSingleItem"), 
    path('report-item/',reportIssue,name="reportIssue"), 
    path('cart/',include('Cart.urls')), 
    path('order/',include('Order.urls')),

]
