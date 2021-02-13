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
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import check_password
from django.core.validators import validate_email
from django.contrib.auth.password_validation import validate_password


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
            if not user.is_superuser and user.is_active:
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
            messages.error(request, 'Some error occured try after sometime')
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
    



def logout(request):
    if (request.session.get('user') != None):
        #print("exist")
        request.session.delete()
        return redirect('Home:home')
    else:
        return redirect('Authentication:login')
 
    # return render(request,template)

#################################

def profile(request):
    template = "account/profile.html"
    context={
        "is_creative":True,
    }
    return render(request, template, context)


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

@login_required
def dashboard(request):
    template = "account/dashboard/dashboard.html"
    return render(request, template)


def add_document(request):
    template = "account/dashboard/document.html"
    return render(request, template)

@login_required
def dashboard_profile(request,action=None):
    template = "account/dashboard/dashboard-profile.html"
    UserFormData=EditUserFormData()
    profileFormData=EditProfileForm()
    
    #print(request.FILES)
    #print(action)
    if request.method == "POST" and action == "editImage":
        #print(request.POST)
        profileForm = EditProfileImage(request.POST or None ,request.FILES or None, instance=request.user.profile)
     
        if profileForm.is_valid():
            #Profile.user_image.delete()
            #profileForm.save()
            #print(request.FILES)
            if request.FILES.get('user_image', None) != None:
                try:
                    old_img = Profile.objects.get(user_id=request.user.user_id).user_image
                    
                    if old_img:
                        os.remove(old_img.path)
                except Exception as e:
                    messages.error(request,"Some error occured during image upload. Refreash page and try again please."+str(e))
                else:
                    request.user.profile.user_image = request.FILES['user_image']
                    request.user.profile.save()
                    messages.success(request,"Profile Image Change Successfully.")
                    return redirect('Authentication:dashboard_profile')                  
        else:
            err=profileForm.errors['user_image']
            messages.error(request,err)
    
    if action == "removeImage":       
        try:
            old_img = Profile.objects.get(user_id=request.user.user_id).user_image
            if old_img:
                os.remove(old_img.path)
        except Exception as e:
            messages.error(request,"Some error occured during image upload. Refreash page and try again please.")
        else:
            old_img = Profile.objects.get(user_id=request.user.user_id)
            old_img.user_image=None
            old_img.save()
            messages.success(request,"Profile Image Change Successfully.")
            return redirect('Authentication:dashboard_profile')    
##################################################################################
    if request.method == "POST" and action == "editProfile":
        #print(request.POST)
        profileFormData = EditProfileForm(request.POST or None, instance=request.user.profile)
        UserFormData = EditUserFormData(request.POST or None, instance=request.user)

        if UserFormData.is_valid() and profileFormData.is_valid():
            
            UserFormData.save()
            #profileFormData.save()

            request.user.profile.bio = request.POST.get("bio")
            request.user.profile.user_gender = request.POST.get("user_gender")
            request.user.profile.save()
          
            #mPr = Profile(request.user.profile.user_id)
            #mPr.bio=request.POST.get("bio")
            #mPr.user_gender = request.POST.get("user_gender")
            #mPr.save()
            
            messages.success(request,"Updated Successfully.")
            UserFormData=EditUserFormData()
            profileFormData=EditProfileForm()
            return redirect('Authentication:dashboard_profile')                  
            
        else:
            messages.warning(request,"Please correct above errors.")
            
    context={
        "Userform":UserFormData,
        "Profileform":profileFormData,
    }
    
    return render(request, template,context)


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

######################## ACCOUNT SETTING ###########################
@login_required
def dashboard_settings(request):
    template = "account/dashboard/settings.html"
    return render(request, template)

@login_required
def changePassword(request):
    template = 'account/dashboard/settings.html'
    #print('GET')
    if request.method == 'POST':
        #print(request.POST)
        old = request.POST['password']
        pass1 = request.POST['password1']
        pass2 = request.POST['password2']
        if pass1 == pass2:
            if 'user' in request.session:
                #print('got session')
                email = request.session.get('user_email')
                #print(email)
                try:
                    print(pass1)
                    #validate_password(pass1) # for length and strength check
                except Exception as e:
                    messages.error(request,*e)
                    return redirect('Authentication:changePassword')
                else:
                    usr = User.objects.get(email__iexact=email)
                    
                    if check_password(old,usr.password):
                        # print('old and new same')
                        usr.set_password(pass1)
                        usr.save()
                        request.session.delete()
                        return redirect('Authentication:login')
                    else:
                        messages.error(request,"Old Password is incorrect.")
                        return redirect('Authentication:changePassword')

        else:
            messages.error(request,"Passwords do not match.")
            return redirect('Authentication:changePassword')

    return render(request,template)

def passwordReset(request):
    template="account/password_reset.html"
    #print(request.POST)
    if request.method == 'POST':
        email = request.POST.get('email',None)
        try:
            validate_email(email)
        except Exception as e:
            print(e)
            messages.error(request,*e)
        else:
            is_email = User.objects.filter(email__iexact=email).exists()
            if is_email:
                usr = User.objects.get(email__iexact=email)
                current_site = get_current_site(request)
                mail_subject = 'Password Reset Link'
                message = render_to_string('account/password_reset_email.html', {
                    'user': usr,
                    'domain': current_site.domain,
                    'uid':urlsafe_base64_encode(force_bytes(usr.user_id)),
                    'token':account_activation_token.make_token(usr),
                })
                to_email = email
                sendemailmsg = EmailMessage(
                            mail_subject, message, to=[to_email]
                )
                #print(sendemailmsg)
                sendemailmsg.send()
                #request.session.delete()
                request.session["reset_password_EMAIL"] = email
                return redirect("Authentication:passwordResetLink")

    return render(request,template)

    

def passwordResetLink(request):
    template="account/password_reset_done.html"
    return render(request,template)

def resetVerified(request,uidb64,token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        return redirect("Authentication:newPassword")
        #return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    else:
        return render(request,"account/account_active_email_done.html",{"activated":False})

def newPassword(request):
    template="account/password_reset_from_key.html"
    if request.method == 'POST':
        password = request.POST.get('password1',None)
        c_password = request.POST.get('password2',None)

        if password == c_password:
            email = request.session.get('reset_password_EMAIL')
            if email:
                try:
                    print(password)
                    #validate_password(pass1) # for length and strength check
                except Exception as e:
                    messages.error(request,*e)
                else:

                    usr = User.objects.get(email=email)
                    usr.set_password(password)
                    usr.save()
                    request.session.delete()
                    return redirect('Authentication:newPasswordDone')
            else:
                return render(request,"account/account_active_email_done.html",{"activated":False})

    return render(request,template)

def newPasswordDone(request):
    template="account/password_reset_from_key_done.html"
    return render(request,template)

@login_required
def deactiveAccount(request):
    template = 'account/dashboard/settings.html'
    if request.method == "POST":
        givenEmail  = request.POST.get("email",None)
        is_email = User.objects.filter(email__iexact=givenEmail).exists()
        if is_email:
            emailSess = request.session.get('user_email')
            try:
                validate_email(givenEmail)
            except Exception as e:
                print(e)
                messages.error(request,*e)
            else:
                usr = User.objects.get(email=givenEmail)
                
                if emailSess == usr.email:
                    #print(emailSess,usrEmail)
                    #user = request.user
                    usr.is_active=False
                    usr.save()
                    #messages.success(request,"Success")
                    return redirect('Home:home')
                else:
                    messages.error(request,"Please enter your registered email.")
                    return redirect('Authentication:settings')
        else:
            messages.error(request,"Please enter your registered email.")
            return redirect('Authentication:settings')
    return render(request,template)


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


