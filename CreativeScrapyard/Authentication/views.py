from django.shortcuts import render, redirect
from .models import Photo
from .forms import PhotoForm
from django.http import JsonResponse
from CustomAdmin.models import tbl_crt_categories, tbl_crt_subcategories


# Create your views here.
def profile(request):
    template = "account/profile.html"
    return render(request, template)


def creative_items(request):
    template = "account/dashboard/creative-items.html"
    return render(request, template)


def add_creative_product(request, id=None):
    if request.is_ajax() and id != None:
        crtSubCategory = tbl_crt_subcategories.objects.filter(crt_category=id)
        return JsonResponse(crtSubCategory)

    if request.method == 'GET':
        photos_list = Photo.objects.all()
        crtCategory = tbl_crt_categories.objects.all()
        template = "account/dashboard/add-product.html"
        return render(request, template, {'photos': photos_list, 'crtCategory': crtCategory})
    elif request.method == 'POST':
        form = PhotoForm(request.POST, request.FILES)
        if form.is_valid():
            photo = form.save()
            data = {'id': photo.id, 'is_valid': True, 'name': photo.file.name, 'url': photo.file.url}
        else:
            data = {'is_valid': False}
        return JsonResponse(data)


def product_photo_remove(request, pk):
    Photo.objects.get(pk=pk).delete()
    return redirect('Authentication:add_creative_product')


def dashboard(request):
    template = "account/dashboard/dashboard.html"
    return render(request, template)


def add_document(request):
    template = "account/dashboard/document.html"
    return render(request, template)


def dashboard_profile(request):
    template = "account/dashboard/dashboard-profile.html"
    return render(request, template)


def order_creative(request):
    template = "account/dashboard/creative-orders.html"
    return render(request, template)


def order_history(request,action='current'):
    if action == 'current':
        title = "Current Orders"
    elif action == 'complete':
        title = "Completed Orders"
    elif action == 'cancel':
        title = "Cancelled Orders"
    elif action == 'return':
        title = 'Returned Orders'


    template = "account/dashboard/order-history.html"
    return render(request, template, {'title': title})


def order_details(request):
    template = "account/dashboard/order-details.html"
    return render(request, template)


def dashboard_settings(request):
    template = "account/dashboard/settings.html"
    return render(request, template)
