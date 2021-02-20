from django.http.request import QueryDict
from CreativeScrapyard import settings
from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse,HttpResponse
import mimetypes,os
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from wsgiref.util import FileWrapper
from django.utils.encoding import smart_str
from .models import *
from Authentication.models import *
from Home.models  import Query
from .forms import *
from django.http import HttpResponseNotFound
from django.core.exceptions import PermissionDenied
from django.http import Http404
from django.core import serializers
from django.contrib.auth import authenticate,login
from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.contrib.auth.hashers import check_password
from django.core.validators import validate_email
from django.contrib.auth.password_validation import validate_password

####### AUTH RELATED #######
def AdminLogin(request):
    template = 'custom-admin/login.html'
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username,password=password)
        # print(user)
        if user:
            #user = User.objects.get(username=username)
            #print(user)
            if user.is_superuser and user.is_active:
                # print(request.user)
                user_sess = {'user_name':user.username,'user_email':user.email}
                #print(user_sess)
                request.session['user'] = user_sess
                request.session['user_email'] = user.email
                login(request, user)
                return redirect('CustomAdmin:adminindex')
            else:
                messages.error(request, 'Invalid Credentials, Try Again.')
        else:
            messages.error(request, 'Invalid Credentials, Try Again.')

        # if user=='admin' and pwd=='admin':
            
        #     request.session['admin'] = user
        #     return redirect('CustomAdmin:adminindex')

    return render(request,template)

def adminindex(request):
    if request.user.is_superuser:
        template='custom-admin/admin-dashboard.html'
        
        return render(request,template)
    else:
        return redirect('CustomAdmin:login')

def adminAccount(request):
    if request.session.get('user'): 
        template = 'custom-admin/account-settings/admin-account.html'
        # admin = request.user.is_authenticated
        # context={
        #     "admin":admin
        # }
        adminFormData = AdminForm()
       
        if request.method == 'POST':

            adminFormData = AdminForm(request.POST, instance=request.user)
        

            #print(request.POST)
            # #print(adminFormData.errors.get_json_data())
            if adminFormData.is_valid():
                adminFormData.save()
                messages.success(request,"Updated Successfully.")
                adminFormData=AdminForm()
                return redirect("CustomAdmin:adminAccount")

            else:
                # errors=adminFormData.errors.get_json_data()
                messages.warning(request,"Please correct above errors.")
                #print(errors)
                #print(adminFormData.errors.get_json_data())

        context={
            "form":adminFormData,
            
        }
        #print(adminFormData)
        return render(request,template,context)
    else:
        return redirect('CustomAdmin:login')

@login_required        
def changePassword(request):
    if request.session.get('user'):    
        template = 'custom-admin/account-settings/change-password.html'

        if request.method == 'POST':
            print(request.POST)
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
                        return redirect('CustomAdmin:changePassword')
                    else:
                        usr = User.objects.get(email__iexact=email)
                        
                        if check_password(old,usr.password):
                            # print('old and new same')
                            usr.set_password(pass1)
                            usr.save()
                            request.session.delete()
                            return redirect('CustomAdmin:login')
                        else:
                            messages.error(request,"Old Password is incorrect.")
                            return redirect('CustomAdmin:changePassword')

            else:
                messages.error(request,"Passwords do not match.")
                return redirect('CustomAdmin:changePassword')

        return render(request,template)
    else:
        return redirect('CustomAdmin:login')

def logout(request):
    if (request.session.get('user') != None):
        request.session.delete()
        return redirect('CustomAdmin:login')
    else:
        return redirect('CustomAdmin:login')



####### USERS RELATED #######

def users(request):
    if request.user.is_superuser:
        template = 'custom-admin/users/users.html'
        user=User.objects.filter(is_superuser=False)
        context={
            "Users":user,
        }

        return render(request,template,context)
    else:
        return redirect('CustomAdmin:login')

def buyers(request):
    if  request.user.is_superuser: 
        template = 'custom-admin/users/buyers.html'
        buyers = User.objects.filter(is_superuser=False,is_active=True)
        context = {
            "buyers":buyers,
        }
        return render(request,template,context)
    else:
        return redirect('CustomAdmin:login')

def sellers(request):
    if  request.user.is_superuser: 
        template = 'custom-admin/users/sellers.html'
        #user=User.objects.filter(is_superuser=False)
        
        #user=User.objects.filter(is_superuser=False,is_active=True)
        #print(user)
        sellers = Profile.objects.filter(is_verified=True)

        context={
            "sellers":sellers,
        }

        return render(request,template,context)
    else:
        return redirect('CustomAdmin:login')

def verifyusers(request,tab="pending"):
    if request.session.get('user'): 
        template = 'custom-admin/users/verify-users.html'
        context={}
        if tab=='pending':
            is_verified=False
            # get data from user documents
            pendingUser = True  # objects of user document
            verifiedUser=""
            
        elif tab == 'verified':
            is_verified=True
            verifiedUser = Profile.objects.filter(is_verified=True)
            pendingUser=False
            
            
      
        context={
            "is_verified":is_verified,
            "verifiedUser":verifiedUser,
            "pendingUser":pendingUser,
        }
        print(context)
        return render(request,template,context)
    else:
        return redirect('CustomAdmin:login')

####### AJAX VERIFY USERS #######
def viewDets(request):
    if request.session.get('user'): 
        data={"bankName":"SBI","bankifscCode":"ABC0123","accNo":"1234567890","accName":"Dummy Dummy",\
            "panNo":"ABCD123456","panName":"Dummy Dummy"}
        return JsonResponse(data)
    else:
        return redirect('CustomAdmin:login')

def docuDownload(request):
    if request.session.get('user'): 
        filename = 'pansample.jpeg'
        file_path = settings.MEDIA_ROOT + '/documents/' + filename

        file_wrapper = FileWrapper(open(file_path,'rb'))       
        file_mimetype = mimetypes.guess_type(file_path)
        response = HttpResponse(file_wrapper, content_type=file_mimetype )
        response['X-Sendfile'] = file_path
        response['Content-Length'] = os.stat(file_path).st_size
        response['Content-Disposition'] = 'attachment; filename=%s' % smart_str(filename) 
        return response
    else:
        return redirect('CustomAdmin:login')

def verifyChk(request):
    if request.session.get('user'): 
        data={"is_verified":True}
        return JsonResponse(data)
    else:
        return redirect('CustomAdmin:login')

####### PRODUCTS RELATED #######
### CREATIVE ###

def creativeCat(request,id=None,action=None):
    if request.session.get('user'):
        crtMainCats=tbl_crt_categories.objects.all()
        template = 'custom-admin/products/creativecategory.html' 
        mainCrtCat=MainCreativeCategoryForm() #remove this just for testing...
        if id != None and action==None :
            #print("DD1")
            subCrtCats=tbl_crt_subcategories.objects.filter(crt_category_id=id)
            parentCat=get_object_or_404(tbl_crt_categories,pk=id)
                
            if subCrtCats!= None:
                return render(request,template,{"subCrtCats":subCrtCats,"mainCat":crtMainCats,"parentCat":parentCat, "dispSubCat":True })
            else:
                return render(request,template,{"subCrtCats":subCrtCats,"mainCat":crtMainCats, "parentCat":parentCat,"dispSubCat":True })

        elif action=="addMain":
            if request.method=="POST" and request.is_ajax():
            #if request.method=="POST":
                
                mainCrtCat=MainCreativeCategoryForm(request.POST or None)

                if mainCrtCat.is_valid():
                    #main_crt_Cat = mainCrtCat.cleaned_data['crt_category_name']
                    try:
                        mainCrtCat.save()
                    except:
                        # print(e)
                        return JsonResponse({"saved":False,"message":"Database Error!!"})
                    
                    return JsonResponse({"saved":True,"message":""})
                else:
                    # print(mainCrtCat.errors.get_json_data(escape_html=True))

                    err=mainCrtCat.errors.get_json_data(escape_html=True)
                    #print(mainCrtCat)
                    #print(err)
                    err=err['__all__'][0]['message']
                    #print(err)
                    #print(mainCrtCat.errors)
                    
                    #print("DD2")
                    return JsonResponse({"saved":False,"message":err})
                    
                    #return render(request,template,{"dispSubCat":False,"mainCat":crtMainCats,"form":mainCrtCat})

            else:
                raise PermissionDenied
            
        elif action=="addCrtSub" and id!=None:
           # print("DD3")
            if request.method=="POST" and request.is_ajax():
                
                newSubCrtCat=SubCreativeCategoryForm(request.POST or None)
                
                if newSubCrtCat.is_valid():
                    #sub_crt_Cat = newSubCrtCat.cleaned_data['crt_sub_category_name']
                    newSubCrtCat = newSubCrtCat.save(commit=False)
                    newSubCrtCat.crt_category = get_object_or_404(tbl_crt_categories, pk=id)
                    try:
                        newSubCrtCat.save()
                    except:
                        return JsonResponse({"saved":False,"message":"Database Error!!"})
                    return JsonResponse({"saved":True,"message":""})
                else:
                    err=newSubCrtCat.errors.get_json_data(escape_html=True)
                    err=err['__all__'][0]['message']
                    return JsonResponse({"saved":False,"message":err})                    
                    
            else:
                raise PermissionDenied
               # return HttpResponseNotFound("404 Page not found.")
        
        elif action=="editMain" and id!=None:

            if request.method=="POST" and request.is_ajax():
               # print("editmain")
                editMainCrtCat = get_object_or_404(tbl_crt_categories, pk=id)
                editMainCrtCat = MainCreativeCategoryForm(request.POST or None,instance=editMainCrtCat)
                if editMainCrtCat.is_valid():
                    try:
                        editMainCrtCat.save()
                    except:
                        return JsonResponse({"updated":False,"message":"Database Error!!"})
                    return JsonResponse({"updated":True,"message":""})
                else:
                    err=editMainCrtCat.errors.get_json_data(escape_html=True)
                    err=err['__all__'][0]['message']
                    return JsonResponse({"saved":False,"message":err})  

            elif request.method=="GET" and request.is_ajax():
                print("ajax")
                mainCrtCat = get_object_or_404(tbl_crt_categories, pk=id)
                return JsonResponse({"crt_category_name":mainCrtCat.crt_category_name})
            else:
                raise PermissionDenied
        
        elif action=="editSubs" and id!=None:
            #print("EditSubs")
            if request.method=="POST" and request.is_ajax():
                editSubCrtCat = get_object_or_404(tbl_crt_subcategories, pk=id)
                editSubCrtCat = SubCreativeCategoryForm(request.POST or None,instance=editSubCrtCat)
                if editSubCrtCat.is_valid():
                    try:
                        editSubCrtCat.save()
                    except:
                        return JsonResponse({"updated":False,"message":"Database Error!!"})
                    return JsonResponse({"updated":True,"message":""})
                else:
                    err=editSubCrtCat.errors.get_json_data(escape_html=True)
                    err=err['__all__'][0]['message']
                    return JsonResponse({"saved":False,"message":err})                     
            elif request.method=="GET" and request.is_ajax():
                #print("ajax")
                subCrtCat = get_object_or_404(tbl_crt_subcategories, pk=id)
                return JsonResponse({"crt_sub_category_name":subCrtCat.crt_sub_category_name})

            else:
                raise PermissionDenied
      
        elif action=="delMain" and id!=None:
            #print("DelMain")
            if request.method=="POST" and request.is_ajax():
                delMainCrtCat = get_object_or_404(tbl_crt_categories, pk=id)
                try:
                    itemName=delMainCrtCat.crt_category_name
                    delMainCrtCat.delete()
                except:
                    return JsonResponse({"saved":False,"message":"Database Error!!"})
                return JsonResponse({"saved":True,"itemName":itemName,"message":""})
   
            else:
                raise PermissionDenied
        elif action=="delSubs" and id!=None:
            #print("DelMain")
            if request.method=="POST" and request.is_ajax():
                delSubCrtCat = get_object_or_404(tbl_crt_subcategories, pk=id)
                try:
                    itemName=delSubCrtCat.crt_sub_category_name
                    delSubCrtCat.delete()
                except:
                    return JsonResponse({"saved":False,"message":"Database Error!!"})
                return JsonResponse({"saved":True,"itemName":itemName,"message":""})
   
            else:
                raise PermissionDenied
                            
        
        return render(request,template,{"dispSubCat":False,"mainCat":crtMainCats,"form":mainCrtCat})
    else:
        return redirect('CustomAdmin:login')



def creativeitems(request):
    if request.session.get('user'):    
        template = 'custom-admin/products/creativeitems.html'
        return render(request,template,{"dispSubCat":False})
    else:
        return redirect('CustomAdmin:login')

############################################
### SCRAP ###
def scrapCat(request,id=None,action=None):
   # print("SCRAPCAT FUNC")
    if request.session.get('user'):   
        scpMainCats=MainScrapCategory.objects.all() 
        template = 'custom-admin/products/scrapcategory.html'
        print("OUT")
        if id != None and action==None :
            print("DD1")
            subScpCats=SubScrapCategory.objects.filter(scp_category_id=id)
            parentCat=get_object_or_404(MainScrapCategory,pk=id)
                
            if subScpCats!= None:
                return render(request,template,{"subScpCats":subScpCats,"mainCat":scpMainCats,"parentCat":parentCat, "dispSubCat":True })
            else:
                return render(request,template,{"subScpCats":subScpCats,"mainCat":scpMainCats, "parentCat":parentCat,"dispSubCat":True })

        elif action=="addMain":
         #   print("DD2")
            if request.method=="POST" and request.is_ajax():
                mainScpCat=MainScrapCategoryForm(request.POST or None)
                if mainScpCat.is_valid():
                    #main_crt_Cat = mainScpCat.cleaned_data['crt_category_name']
                    try:
                        mainScpCat.save()
                    except:
                        return JsonResponse({"saved":False,"message":"Database Error!!"})
                    
                    return JsonResponse({"saved":True,"message":""})
                else:
                    return JsonResponse({"saved":False,"message":"Invalid Data!!"})
            else:
                raise PermissionDenied
            
        elif action=="addScpSub" and id!=None:
            
         #   print("DD3")
            if request.method=="POST" and request.is_ajax():
                
                newSubScpCat=SubScrapCategoryForm(request.POST or None)
                if newSubScpCat.is_valid():
                    #sub_crt_Cat = newSubScpCat.cleaned_data['crt_sub_category_name']
                    newSubScpCat = newSubScpCat.save(commit=False)
                    newSubScpCat.scp_category = get_object_or_404(MainScrapCategory,pk=id)
                    try:
                        newSubScpCat.save()
                    except:
                        return JsonResponse({"saved":False,"message":"Database Error!!"})
                    return JsonResponse({"saved":True,"message":""})
                else:
                    return JsonResponse({"saved":False,"message":"Invalid Data!!"})
            else:
                raise PermissionDenied
               # return HttpResponseNotFound("404 Page not found.")
        
        elif action=="editMain" and id!=None:

            if request.method=="POST" and request.is_ajax():
            #    print("editmain")
                editMainScpCat = get_object_or_404(MainScrapCategory,pk=id)
                editMainScpCat = MainScrapCategoryForm(request.POST or None,instance=editMainScpCat)
                if editMainScpCat.is_valid():
                    try:
                        editMainScpCat.save()
                    except:
                        return JsonResponse({"updated":False,"message":"Database Error!!"})
                    return JsonResponse({"updated":True,"message":""})
                else:
                    return JsonResponse({"updated":False,"message":"Invalid Data!!"})
            elif request.method=="GET" and request.is_ajax():
            #    print("ajax")
                mainScpCat = get_object_or_404(MainScrapCategory,pk=id)
                return JsonResponse({"scp_category_name":mainScpCat.scp_category_name})
            else:
                raise PermissionDenied
        
        elif action=="editSubs" and id!=None:
         #   print("EditSubs")
            if request.method=="POST" and request.is_ajax():
                editSubScpCat = get_object_or_404(SubScrapCategory,pk=id)
                editSubScpCat = SubScrapCategoryForm(request.POST or None,instance=editSubScpCat)
                if editSubScpCat.is_valid():
                    try:
                        editSubScpCat.save()
                    except:
                        return JsonResponse({"updated":False,"message":"Database Error!!"})
                    return JsonResponse({"updated":True,"message":""})
                else:
                    return JsonResponse({"updated":False,"message":"Invalid Data!!"})
            elif request.method=="GET" and request.is_ajax():
             #   print("ajax")
                subScpCat = get_object_or_404(SubScrapCategory,pk=id)
                return JsonResponse({"scp_sub_category_name":subScpCat.scp_sub_category_name})

            else:
                raise PermissionDenied
      
        elif action=="delMain" and id!=None:
          #  print("DelMain")
            if request.method=="POST" and request.is_ajax():
                delMainScpCat = get_object_or_404(MainScrapCategory,pk=id)
                try:
                    itemName=delMainScpCat.scp_category_name
                    delMainScpCat.delete()
                except:
                    return JsonResponse({"saved":False,"message":"Database Error!!"})
                return JsonResponse({"saved":True,"itemName":itemName,"message":""})
   
            else:
                raise PermissionDenied
        elif action=="delSubs" and id!=None:
         #   print("DelMain")
            if request.method=="POST" and request.is_ajax():
                delSubScpCat = get_object_or_404(SubScrapCategory,pk=id)
                try:
                    itemName=delSubScpCat.scp_sub_category_name
                    delSubScpCat.delete()
                except:
                    return JsonResponse({"saved":False,"message":"Database Error!!"})
                return JsonResponse({"saved":True,"itemName":itemName,"message":""})
   
            else:
                raise PermissionDenied
        return render(request,template,{"dispSubCat":False,"mainCat":scpMainCats})

    else:
        return redirect('CustomAdmin:login')

        
def scrapitems(request):
    if request.session.get('user'):    
        template = 'custom-admin/products/scrapitems.html'
        return render(request,template)
    else:
        return redirect('CustomAdmin:login')

####### ORDERS RELATED #######
def allorders(request):
    if request.session.get('user'):    
        template = 'custom-admin/allorders.html'
        return render(request,template)
    else:
        return redirect('CustomAdmin:login')


def orderdetails(request,id):
    if request.session.get('user'):    
        template = 'custom-admin/orderdetails.html'
        return render(request,template)
    else:
        return redirect('CustomAdmin:login')

def allorderdetails(request,action='delivered'):
    
    if request.session.get('user'):  
        #print(action)
        if action == 'delivered':
            title = "Delivered Orders"
        elif action == 'returned':
            title = "Returned Orders"
        elif action == 'processing':
            title = "Processing Orders"
        elif action == 'canceled':
            title = "Cancelled Orders"
        
        template = 'custom-admin/allorderdetails.html'
        return render(request,template,{"title":title})
    else:
        return redirect('CustomAdmin:login')

#######    PAYMENT     #######

def payment(request):
    if request.session.get('user'):    
        template = 'custom-admin/payment.html'
        return render(request,template)
    else:
        return redirect('CustomAdmin:login')
####### BADGES RELATED #######
def badges(request):
    if request.session.get('user'):    
        template = 'custom-admin/manage-badges.html'
        return render(request,template)

    else:
        return redirect('CustomAdmin:login')

####### QUERIES RELATED #######
def queries(request):
    if request.user.is_superuser:    
        template = 'custom-admin/queries/queries.html'
        Qry = Query.objects.all()


        context={
            "queries":Qry,
        }
        return render(request,template,context)

    else:
        return redirect('CustomAdmin:login')    

def issues(request,opts="reportedCrtItem"):
    if request.session.get('user'):    
        template = 'custom-admin/queries/issues.html'
        title = "Reported Creative Items"
        issueType=1
        columnName="Item SKU"
        if request.method=="POST":
            issueType=request.POST.get("issueType")

            if issueType == '1':
                title = "Reported Creative Items"
                issueType=1
                columnName="Item SKU"
            elif issueType == '2' :
                title= "Reported Scrap Items"
                issueType=2
                columnName="Item SKU"
            elif issueType == '3' :
                title =  "Reported Users Items"
                issueType=3
                columnName="Username"
            elif issueType == '4':
                title = "Order Issues" 
                issueType=4    
                columnName="Oreder Detail ID"      
        
        context = {
            "title":title,
            "issueType":issueType,
            "columnName":columnName,
            
        }
        return render(request,template,context)

    else:
        return redirect('CustomAdmin:login')
####### SEND EMAIL RELATED #######
@login_required
def sendmail(request):
    if request.session.get('user'):    
        template = 'custom-admin/sendmail/sendmail.html'
       
        if request.method == "POST" and not request.is_ajax():
            email = request.POST.get('email', '')
            subject = request.POST.get('subject', '')
            emailmessage = request.POST.get('message', '')
            print(request.POST)
            if not subject or not emailmessage:
                messages.error(request,"Subject or message cannot be empty.")
                return redirect("CustomAdmin:sendmail")
            else:
                #print(email.split(","),subject,emailmessage)
                try:
                    emailList=email.split(",")
                    current_site = get_current_site(request)
                    mail_subject = subject
                    message = render_to_string('common/email.html', {
                        'message':str("\n")+emailmessage,
                        # 'user':User.objects.get(email__iexact=email)
                    })
                    # to_email = emailList
                    email = EmailMessage(
                                mail_subject, message, to=emailList
                    )
                    email.send()
                
                except Exception as e:
                    messages.error(request,"Some error occured. Please try after sometime."+str(e))
                finally:
                    return redirect("CustomAdmin:sendmail")


        if request.is_ajax() and request.method=="POST":
            # print(request.POST)
            email = request.POST.get('email', '')
            emailmessage = request.POST.get('message', '')
            typeFor = request.POST.get('type', '')

            if not email or not emailmessage:
                return JsonResponse({"send":True,"msg":"empty email field is not allowed."})
            else:
                if typeFor == "user":
                    #print(email.split(","),subject,emailmessage)
                    try:
                        emailList=email.split(",")
                        current_site = get_current_site(request)
                        mail_subject = "Your account is disabled"
                        message = render_to_string('common/email.html', {
                            'message':str("\n")+emailmessage,
                            'user':User.objects.get(email__iexact=email),
                            'type':"user",
                        })
                        to_email = email
                        email = EmailMessage(
                                    mail_subject, message, to=emailList
                        )
                        email.send()
                    
                    except Exception as e:
                        return redirect({"send":True,"msg":str(e)})           
                    else:
                        return JsonResponse({"send":True,"msg":"Mail Sent"})
                elif typeFor == "product":
                    try:                
                        emailList=email.split(",")
                        current_site = get_current_site(request)
                        mail_subject = "Your Product is disabled"
                        message = render_to_string('common/email.html', {
                            'message':str("\n")+emailmessage,
                            'user':User.objects.get(email__iexact=email),
                            'type':"product"
                            # here get the product obj
                        })
                        to_email = email
                        email = EmailMessage(
                                    mail_subject, message, to=emailList
                        )
                        email.send()
                
                    except Exception as e:
                        return redirect({"send":True,"msg":str(e)})           
                    else:
                        return JsonResponse({"send":True,"msg":"Mail Sent"})
                
                    
            #return JsonResponse({"send":True,"msg":"Mail Sent"})



        return render(request,template)
    else:
        return redirect('CustomAdmin:login')    

####### REPLY QRY ####################

@login_required
def replyQry(request,id):
    if request.user.is_superuser:    
        template = 'custom-admin/queries/queries.html'
       
        if request.method == "POST" and not request.is_ajax():
            # email = request.POST.get('email', '')
            subject = request.POST.get('subject', '')
            emailmessage = request.POST.get('message', '')
            print(request.POST)
            if not subject or not emailmessage:
                messages.error(request,"Subject or message cannot be empty.")
                return redirect("CustomAdmin:query")
            else:
                #print(email.split(","),subject,emailmessage)
                try:
                    qtyObj = Query.objects.get(query_id=id)
                    #emailList=email.split(",")
                    current_site = get_current_site(request)
                    mail_subject = subject
                    message = render_to_string('common/email.html', {
                        'message':str("\n")+emailmessage,
                        'QrySender':qtyObj,
                        'type':'queryReply',
                        
                    })
                    # to_email = emailList
                    email = EmailMessage(
                                mail_subject, message, to=[qtyObj.email]
                    )
                    email.send()
                
                except Exception as e:
                    messages.error(request,"Some error occured. Please try after sometime.")
                finally:
                    return redirect("CustomAdmin:query")



        return render(request,template)
    else:
        return redirect('CustomAdmin:login') 



######################################################
# def loadSubCrtCats(request,id=None):
#     if request.session.get('user'):
#         if request.is_ajax() :
#             main={"mainCatName":[{"Home Decor":["a","b","c"]},{"LifeStyle-Men":["d","e","f","g"]}]}
#             return JsonResponse(main)
#         template = 'custom-admin/products/creativecategory.html' 
#         if (id==1):
#             main={"mainCatName":"Home Decor"}
#             subCrtCats={0: {"name" : "1sub dummy1","products":"10" }, 1:{"name" : "1sub dummy2","products":"20" },3:{"name" : "1sub dummy3","products":"0" } }
#         elif (id==2):
#             main={"mainCatName":"LifeStyle-Men"}
#             subCrtCats={0:{"name" : "2sub dummy1","products":"10" }, 1:{"name" : "2sub dummy1","products":"30" } }
#         else:
#             main={"mainCatName":"LifeStyle-Women"}
#             subCrtCats={}
#             return render(request,template,{"subCrtCats":subCrtCats,"mainCat":main, "dispSubCat":True })

#         return render(request,template,{"subCrtCats":subCrtCats,"mainCat":main,"dispSubCat":True})
#     else:
#         return redirect('CustomAdmin:login')