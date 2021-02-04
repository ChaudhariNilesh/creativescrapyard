from django.shortcuts import render
from django.shortcuts import render,redirect
from .forms import QueryForm
from Home.validate import *

# Create your views here.
def home(request):
    template="Home/index.html"
    return render(request,template,{'is_home':True})

def creativestore(request):
    template="Home/creativestore.html"
    return render(request,template,{'is_creative':True})    

def scrapyard(request):
    template="Home/scrapyard.html"
    return render(request,template,{'is_scrap':True})    

def achievers(request):
    template="achievers.html"
    return render(request,template,{'is_creative':True})    

def login(request):
    template="Home/login.html"
    return render(request,template)

def signup(request):
    template="Home/registration.html"
    return render(request,template)

def contactus(request):
    template="contact-us.html"
    formData = QueryForm()
    if request.method == 'POST':
        formData = QueryForm(request.POST or None)
        mail = request.POST['contactEmail']
        # name = request.POST['contactName']
        name = "Nikul"
        context = validate(email=mail, name=name)
        print(context)
        context['is_creative'] = True
        #
        # is_valid = checkEmail(mail)
        # nameValid = checkName(name)
        # context = {
        #     'emailValid': is_valid
        # }
        return render(request, template, context)

    return render(request,template,{'is_creative':True})


def aboutus(request):
    template="about-us.html"
    return render(request,template,{'is_creative':True})

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