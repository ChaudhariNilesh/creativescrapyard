from django.shortcuts import render,redirect
from CreativeScrapyard import settings
from Authentication.models import Address

# Create your views here.
def checkout(request):
    template="Order/checkout.html"
    
    defaultAddress = Address.objects.get(user_id=request.user.user_id,is_default=True)
    addressList = Address.objects.filter(user_id=request.user.user_id)
    if request.method == "POST":
        addrsId = request.POST.get("addressRadio","")
        defaultAddress = Address.objects.get(address_id=addrsId)
        
    context={
        'is_creative':True,
        'defaultAddress':defaultAddress,
        'addressList':addressList
   }
    return render(request,template,context)

def orderHistory(request):
    template="Order/order-history.html"
    return render(request,template,{'is_creative':True})

def orderTrack(request):
    template="Order/order-track.html"
    return render(request,template,{'is_creative':True})