from django.shortcuts import render

# Create your views here.
def addToCart(request):
    template = 'Cart/cart.html'
    return render(request,template,{'is_creative':True})