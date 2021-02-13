from django.shortcuts import render, redirect,HttpResponse
from .models import *
from .forms import *
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .token import account_activation_token
from django.core.mail import EmailMessage
from django.contrib.auth import authenticate,login

# Create your views here.
def UserLogin(request):
    template="Home/login.html"

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username,password=password)
        #print(user)
        if user:
            user = User.objects.get(username=username)
            #print(user)
            if user.is_superuser and user.is_active:
                user_sess = {'user_name':user.username,'user_email':user.email}
                #print(user_sess)
                request.session['user'] = user_sess
                request.session['user_email'] = user.email
                login(request, user)
                return redirect("Home:home")
            else:
                messages.error(request, 'Invalid Credentials, Try Again.')
        else:
            messages.error(request, 'Invalid Credentials, Try Again.')
            
        #return JsonResponse({"account":"no"})
    return render(request,template)

def signup(request):
    template="Home/registration.html"
    if request.method == "GET":
        # userFormData=UserForm()
        # profileFormData=ProfileForm()
        return render(request,template)

    if request.method=="POST":
        #print(request.POST)
        first_name = request.POST.get('first_name', '')
        last_name = request.POST.get('last_name', '')
        username = request.POST.get('username', '')
        gender = request.POST.get('user_gender', '')
        email = request.POST.get('user_email', '')
        password = request.POST.get('user_password', '')

        try:
            #userSignUp = User(username=username,first_name=first_name,\
             #   last_name=last_name,email=email,password=password) 
            userSignUp = User.objects.create_user(username,\
               email,password,first_name=first_name,last_name=last_name)
            userSignUp.is_active=False
            userSignUp.save()
            userProfile = Profile(user_id=userSignUp,user_gender=gender)
            userProfile.save()
            
            current_site = get_current_site(request)
            mail_subject = 'Activate your account.'
            message = render_to_string('account/account_active_email.html', {
                'user': userSignUp,
                'domain': current_site.domain,
                'uid':urlsafe_base64_encode(force_bytes(userSignUp.user_id)),
                'token':account_activation_token.make_token(userSignUp),
            })
            to_email = email
            email = EmailMessage(
                        mail_subject, message, to=[to_email]
            )
            email.send()
            return redirect("Authentication:EmailverificationSent")
        except Exception as e:
            print(e)
            messages.error(request, 'Some error occured try after sometime.')
    return render(request,template)

def EmailverificationSent(request):
    template = 'account/verification_link.html'
    return render(request,template)


def activateAccount(request,uidb64,token):
    template = 'account/account_active_email_done.html'
    
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return render(request,template,{"activated":True})
        #return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    else:
        return render(request,template,{"activated":False})


# def activateAccountDone(request):
#     template = 'account/account_active_email_done.html'
#     return render(request,template)
    

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

def logout(request):
    if (request.session.get('user') != None):
        print("exist")
        request.session.delete()
        return redirect('Home:home')
    else:
        return redirect('Authentication:login')

    # return render(request,template)

#################################

def profile(request):
    template = "account/profile.html"
    return render(request, template)


def creative_items(request):
    template = "account/dashboard/creative-items.html"
    return render(request, template)

def scrap_items(request):
    template = "account/dashboard/scrap-items.html"
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

def dashboard_payments(request):
    template = "account/dashboard/payments.html"
    return render(request, template)


def dashboard_settings(request):
    template = "account/dashboard/settings.html"
    return render(request, template)



def add_document(request):
    if request.session.get('user'):
        template = "account/dashboard/document.html"
        documentData=UserDocument()
        if request.method=='POST':
            documentData=UserDocument(request.POST,instance=request.user)
            if documentData.is_valid():
                print("Heloo")

            else:
                print(documentData.errors)
                messages.warning(request,"Please correct above errors.")
            
        context={
            "form":documentData,
        }
        return render(request,template,context)
    else:
        return redirect('Authentication:login')

def editDocument(request):
    if request.session.get('user'): 
        template = 'account/dashboard/dashboard-profile.html'
        editedData=EditUserDocument()
        if request.method=='POST':
            editedData=EditUserDocument(request.POST, instance=request.user)
            if editedData.is_valid():
                print("hello world")
               # addressFormData.save()
               # messages.success(request,"Updated Successfully.")
               # addressFormData=AddressForm()
               # redirect("Authentication:dashboard_profile")

            else:
                print(editedData.errors)
                messages.warning(request,"Please correct above errors.")
            
        context={
            "form":editedData,
        }
        return render(request,template,context)
    else:
        return redirect('Authentication:login')




def addAddress(request):
    if request.session.get('user'): 
        template = 'account/dashboard/add-address.html'
        addressFormData=AddressForm()
        if request.method=='POST':
            addressFormData=AddressForm(request.POST, instance=request.user)
            if addressFormData.is_valid():
                print("hello world")
               # addressFormData.save()
               # messages.success(request,"Updated Successfully.")
               # addressFormData=AddressForm()
               # redirect("Authentication:dashboard_profile")

            else:
                print(addressFormData.errors)
                messages.warning(request,"Please correct above errors.")
            
        context={
            "form":addressFormData,
        }
        return render(request,template,context)
    else:
        return redirect('Authentication:login')


