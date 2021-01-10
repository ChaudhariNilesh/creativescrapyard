from django.shortcuts import render

# Create your views here.
def profile(request):
    template = "account/profile.html"
    return render(request, template,{'is_creative':True})

def creative_items(request):
    template = "account/dashboard/creative-items.html"
    return render(request, template)

def add_creative_product(request):
    template = "account/dashboard/add-product.html"
    return render(request, template)

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

def order_history(request):
    template = "account/dashboard/order-history.html"
    return render(request, template)

def order_details(request):
    template = "account/dashboard/order-details.html"
    return render(request, template)

def settings(request):
    template = "account/dashboard/settings.html"
    return render(request, template)