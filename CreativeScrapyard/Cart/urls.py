from django.urls import path
from django.urls import path,include
from .views import *

app_name = "Cart"

urlpatterns = [
    path('add-to-cart/',addToCart,name="addToCart"), 
    

    path('ajax/change-quantity/',changeQty,name="changeQty"), 
    path('ajax/get-total/',getTotal,name="getTotal"), 
    path('ajax/remove-cart-item/',removeCartItem,name="removeCartItem"), 

    



]
