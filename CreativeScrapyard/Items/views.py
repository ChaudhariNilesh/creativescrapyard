from CreativeScrapyard import settings
from django.shortcuts import render,redirect,HttpResponse
from .forms import *
# Create your views here.

def creativeSingleItem(request):
    template = 'Shop/single-item.html'
    return render(request,template,{'is_creative':True})

def scrapSingleItem(request):
    template = 'Shop/single-item.html'
    return render(request,template,{'is_scrap':True})


def tmp(request):
    template="temp.html"

    if request.method == 'POST':
        form = tbl_creativeitems_mst_form(request.POST or None)

        if form.clean_crt_items_name(request.POST):
            return HttpResponse("DONE")
        else:
            return HttpResponse("FAILED")

    return render(request, template)
