from django.shortcuts import render
from django.shortcuts import render,redirect

# Create your views here.
def home(request):
    template="Home/index.html"
    return render(request,template)