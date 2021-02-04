from django.urls import path
from django.urls import path,include
from .views import *

app_name = "Cart"

urlpatterns = [
    path('add-to-cart/',addToCart,name="addToCart"), 

]
