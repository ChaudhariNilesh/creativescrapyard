from django.shortcuts import render
from Home.validate import*
from django.http import JsonResponse

# Create your views here.

def validationContactForm(request):
    pass

def validationSignUpForm(request):
    #signUpFormData = signUpForm()
    if request.method == "POST":
        #print(request.POST)
        first_name = request.POST.get('first_name', '')
        last_name = request.POST.get('last_name', '')
        username = request.POST.get('username', '')
        user_email = request.POST.get('user_email', '')
        user_gender = request.POST.get('user_gender', '')
        user_password = request.POST.get('user_password', '')
        user_confirm_password = request.POST.get('user_confirm_password', '')

        errorData=validate(email=user_email,username=username,fname=first_name,lname=last_name,\
            pswd1=user_password,pswd2=user_confirm_password,chkTakenEmail=True,chkTakenUsrname=True)
        
        return JsonResponse(errorData)


        #istaken_email = User.objects.filter(email__iexact=email).exists()
            
            #signUpFormData = signUpForm(request.POST)
