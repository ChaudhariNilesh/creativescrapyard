from django.shortcuts import render,redirect
from CreativeScrapyard import settings

# Create your views here.
def checkout(request):
    template="Order/checkout.html"
    return render(request,template,{'is_creative':True})

def orderHistory(request):
    template="Order/order-history.html"
    return render(request,template,{'is_creative':True})

def orderTrack(request):
    template="Order/order-track.html"
    return render(request,template,{'is_creative':True})