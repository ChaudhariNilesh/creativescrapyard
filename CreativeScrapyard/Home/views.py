from django.shortcuts import render
from django.shortcuts import render,redirect

# Create your views here.
def home(request):
    template="Home/index.html"
    return render(request,template)

def creativestore(request):
    template="Home/creativestore.html"
    return render(request,template)    

def login(request):
    template="Home/login.html"
    return render(request,template)

def signup(request):
    template="Home/registration.html"
    return render(request,template)