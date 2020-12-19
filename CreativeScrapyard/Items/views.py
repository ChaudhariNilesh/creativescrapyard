from CreativeScrapyard import settings
from django.shortcuts import render,redirect
# Create your views here.

def singleItem(request):
    template = 'Shop/single-item.html'
    return render(request,template)

def viewCartItem(request):
    template = 'Shop/cart.html'
    return render(request,template)