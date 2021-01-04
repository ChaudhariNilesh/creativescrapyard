from CreativeScrapyard import settings
from django.shortcuts import render,redirect
# Create your views here.

def creativeSingleItem(request):
    template = 'Shop/single-item.html'
    return render(request,template,{'is_creative':True})

def scrapSingleItem(request):
    template = 'Shop/single-item.html'
    return render(request,template,{'is_scrap':True})



