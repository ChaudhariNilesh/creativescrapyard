from django.shortcuts import render
from django.shortcuts import render,redirect

# Create your views here.
def home(request):
    template="Home/index.html"
    return render(request,template)

def creativestore(request):
    template="Home/creativestore.html"
    return render(request,template)    

def scrapyard(request):
    template="Home/scrapyard.html"
    return render(request,template)    

def login(request):
    template="Home/login.html"
    return render(request,template)

def signup(request):
    template="Home/registration.html"
    return render(request,template)

def contactus(request):
    template="contact-us.html"
    return render(request,template)

def passwordReset(request):
    template="account/password_reset.html"
    return render(request,template)

def passwordResetLink(request):
    template="account/password_reset_done.html"
    return render(request,template)

def newPassword(request):
    template="account/password_reset_from_key.html"
    return render(request,template)

def newPasswordDone(request):
    template="account/password_reset_from_key_done.html"
    return render(request,template)