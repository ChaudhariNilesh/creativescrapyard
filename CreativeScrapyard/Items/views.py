from CreativeScrapyard import settings
from django.shortcuts import render,redirect
# Create your views here.

def singleItem(request):
    template = 'common/single-item.html'
    return render(request,template)