from django.shortcuts import render

# Create your views here.
def profile(request):
    template = "account/profile.html"
    return render(request, template)


def add_product(request):
    template = "account/dashboard/add-product.html"
    return render(request, template)

def dashboard(request):
    template = "account/dashboard.html"
    return render(request, template)

def add_document(request):
    template = "account/dashboard/document.html"
    return render(request, template)