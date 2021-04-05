
from django.http.request import QueryDict
from CreativeScrapyard import settings
from django.db import models
from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse,HttpResponse
import mimetypes,os
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from wsgiref.util import FileWrapper
from django.utils.encoding import smart_str
from .models import *
from .forms import *
from Authentication.models import *
from Items.models import *
from Home.models  import Query
from django.core.exceptions import PermissionDenied
from django.http import Http404,HttpResponseForbidden

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
from django.core.serializers import serialize
from django.db.models import Count,Q,Sum,F
from Order.models import *
from Payments.models import *

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
        totalRevenue = tbl_orders_details.objects.filter(item_status=2).aggregate(total = Sum(F('crt_item_qty') * F('unit_price')*0.2,output_field=models.FloatField()))
        currentOrder = tbl_orders_mst.objects.filter(delivery_status=1).count()
        totalOrder = tbl_orders_mst.objects.all().count()
        totalSeller = Profile.objects.filter(is_verified=True,user__is_active=True).count()
        totalUser = User.objects.filter(is_active=True,is_superuser=False).count()
        totalScrapProduct = tbl_scrapitems.objects.filter(scp_item_status="ACTIVE").count()
        totalCreativeProduct = tbl_creativeitems_mst.objects.filter(crt_item_status="ACTIVE").count()

        context = {
            "totalRevenue": totalRevenue,
            "currentOrder": currentOrder,
            "totalOrder": totalOrder,
            "totalSeller": totalSeller,
            "totalUser": totalUser,
            "totalScrapProduct": totalScrapProduct,
            "totalCreativeProduct": totalCreativeProduct,
        }

        return render(request,template, context)
    else:
        return redirect('CustomAdmin:login')

def adminAccount(request):
    if request.user.is_superuser: 
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
    if request.user.is_superuser:    
        template = 'custom-admin/account-settings/change-password.html'

        if request.method == 'POST':
            # print(request.POST)
            old = request.POST['password']
            pass1 = request.POST['password1']
            pass2 = request.POST['password2']
            if pass1 == pass2:
                if 'user' in request.session:
                    #print('got session')
                    email = request.session.get('user_email')
                    #print(email)
                    if bool(re.match('[A-Za-z0-9@#$%^&+=]{9,}',pass1)):
                        try:
                            print(pass1)
                            validate_password(pass1) # for length and strength check
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
                        messages.error(request,"Password does not match given criteria.")
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
        # users = User.objects.filter(is_superuser=False)
        # data = serialize("json",users,fields=("user_id,username,email,date_created,is_active,is_verified"))   ## FOR MODAL OBJECTS
        # # data = list(users.values())
         
        # # print(data)
        
        # user=users.annotate(num_crt = Count('tbl_creativeitems_mst'))
        ########NIKUL############
        # accounts = User.objects.filter(is_superuser=False)
        # for account in accounts:
        #     acc = account.seller_id.all().count()
        #     print(acc)

        users = User.objects.filter(is_superuser=False).annotate(num_crt = Count('tbl_creativeitems_mst',distinct=True),\
            num_scp=Count('tbl_scrapitems',distinct=True))
        

        # print(users.values('num_scp'))
        context={
            "Users":users,
        }

        return render(request,template,context)
    else:
        return redirect('CustomAdmin:login')



def buyers(request):
    if  request.user.is_superuser: 
        template = 'custom-admin/users/buyers.html'

        # buyers = tbl_orders_mst.objects.filter(user__in=users)

        buyerItemCount = tbl_orders_details.objects.filter(item_status=2).values("order__user").annotate(itemCount=Count('crt_item_mst'))
        buyerOrdAmt= tbl_orders_details.objects.filter(item_status=2).values("order__user").annotate(ordAmt=Sum(F('crt_item_qty') * F('unit_price'),output_field=models.FloatField()))
        users = User.objects.filter(is_superuser=False, is_active=True)

        # itemCount = tbl_orders_mst.objects.all().values("user").annotate(itemCount=Sum('tbl_orders_details__crt_item_qty'))
        # print(itemCount)
        # print(users)

        context = {
            "buyers":zip(users,buyerItemCount,buyerOrdAmt),
        }
        return render(request,template,context)
    else:
        return redirect('CustomAdmin:login')

def sellers(request):
    if  request.user.is_superuser: 
        template = 'custom-admin/users/sellers.html'
        #user=User.objects.filter(is_superuser=False)
        
        sellers = Profile.objects.filter(is_verified=True,user__is_active=True)

        sellerItemCount = tbl_orders_details.objects.filter(item_status=2).values("crt_item_mst__user").annotate(itemCount=Count('crt_item_mst'))
        sellerOrdAmt= tbl_orders_details.objects.filter(item_status=2).values("crt_item_mst__user").annotate(ordAmt=Sum(F('crt_item_qty') * F('unit_price'),output_field=models.FloatField()))
        
        
        context={
            "sellers":zip(sellers,sellerItemCount,sellerOrdAmt)
        }

        return render(request,template,context)
    else:
        return redirect('CustomAdmin:login')

def verifyusers(request,tab="pending"):
    if request.user.is_superuser:
        template = 'custom-admin/users/verify-users.html'
        context={}
        if tab=='pending':
            is_verified=False
            verifiedUser=None
            usersSet=Profile.objects.filter(is_verified=False)
            pendingUser = Documents.objects.filter(user__profile__in=usersSet)
                  
            
        elif tab == 'verified':
            is_verified=True
            pendingUser = None
            usersSet=Profile.objects.filter(is_verified=True)
            verifiedUser = Documents.objects.filter(user__profile__in=usersSet)
             

        context={
            "is_verified":is_verified,
            "verifiedUser":verifiedUser,
            "pendingUser":pendingUser,
        }
        # print(context)
        return render(request,template,context)
    else:
        return redirect('CustomAdmin:login')

####### AJAX VERIFY USERS #######
def viewDets(request,docId=None):
    if request.user.is_superuser:
        if request.is_ajax() and docId is not None:
            documentData = Documents.objects.filter(doc_id=docId)
            
            if not documentData:
                raise Http404("404 Not Found")
            
            # data={"bankName":"SBI","bankifscCode":"ABC0123","accNo":"1234567890","accName":"Dummy Dummy",\
            #     "panNo":"ABCD123456","panName":"Dummy Dummy"}
            data={}
            lst=list(documentData.values("acc_no","acc_name","bank_name","IFSC_code","pan_no","pan_name"))
        
            for l in lst: data=(l)
            # print(data)

            return JsonResponse({"documentData":data})
        else:
            raise Http404("404 Not Found")
            
    else:
        return redirect('CustomAdmin:login')

def docuDownload(request,docId=None):
    if request.user.is_superuser: 
        # filename = 'pansample.jpeg'
        # file_path = settings.MEDIA_ROOT + '/documents/' + filename

        # file_wrapper = FileWrapper(open(file_path,'rb'))       
        # file_mimetype = mimetypes.guess_type(file_path)
        # response = HttpResponse(file_wrapper, content_type=file_mimetype )
        # response['X-Sendfile'] = file_path
        # response['Content-Length'] = os.stat(file_path).st_size
        # response['Content-Disposition'] = 'attachment; filename=%s' % smart_str(filename) 

        if docId is not None:
            docuImg = Documents.objects.get(doc_id=docId)
            filename = docuImg.pan_img_url
            # print(filename)

            file_path = filename.path
            file_wrapper = FileWrapper(open(file_path,'rb'))       
            file_mimetype = mimetypes.guess_type(file_path)
            response = HttpResponse(file_wrapper, content_type=file_mimetype )
            response['X-Sendfile'] = file_path
            response['Content-Length'] = os.stat(file_path).st_size
            response['Content-Disposition'] = 'attachment; filename=%s' %(str(docuImg.user.username)+str("_")+smart_str(filename))
             
        return response
    else:
        return redirect('CustomAdmin:login')

def verifyChk(request,action=None,usrId=None):
    if request.user.is_superuser:
        if request.is_ajax() and action is not None and usrId is not None:
            profile = Profile.objects.get(user_id=usrId)
            # print(profile.is_verified)
            
            if action=="accept":
                profile.is_verified = True
                profile.save()
                sendVerifiedMail("verifiedUser",profile,profile.is_verified)
                data={"is_verified":True}
                # print(data) 
            elif action=="reject":
                docu = Documents.objects.get(user=profile.user)
                docu.delete()
                sendVerifiedMail("verifiedUser",profile,profile.is_verified)
                data={"is_verified":False}
                # print(data) 
        else:
            return HttpResponseForbidden("403 Forbidden")

        return JsonResponse(data)
    else:
        return redirect('CustomAdmin:login')

####### PRODUCTS RELATED #######
### CREATIVE ###

def creativeCat(request,id=None,action=None):
    if request.user.is_superuser:
        crtMainCats=tbl_crt_categories.objects.all().order_by("crt_category_name")

     
        mainCrtCnt = tbl_crt_subcategories.objects.values("crt_category__crt_category_name").annotate(CrtCnt=Count('tbl_creativeitems_mst'))
        
        # zipped=zip(crtMainCats, mainCrtCnt)
        # print(crtMainCats)


        template = 'custom-admin/products/creativecategory.html' 
        mainCrtCat=MainCreativeCategoryForm() #remove this just for testing...
        
        # categories = tbl_crt_subcategories.objects.annotate(Count('tbl_creativeitems_mst'))
        # print(categories.values_list('crt_sub_category_name', 'tbl_creativeitems_mst__count'))
       
        # lst= categories.values_list('crt_category_id').distinct(True)#maincat id

        # categories = tbl_crt_subcategories.objects.annotate(itemCount=Count('tbl_creativeitems_mst',distinct=True))
        # print(categories.values_list('crt_sub_category_name', 'tbl_creativeitems_mst__count'))
        # print(categories.values_list('crt_category_id'),categories[0].itemCount)


        if id != None and action==None :
            subCrtCats=tbl_crt_subcategories.objects.filter(crt_category_id=id).annotate(itemCount=Count('tbl_creativeitems_mst')).order_by("crt_sub_category_name")
            # print("DD1")
            # tmp = Count('tbl_creativeitems_mst', filter=Q(tbl_creativeitems_mst__crt_sub_category=subCrtCats.values('crt_sub_category_id')))
            # print(tmp)
            # categories= tbl_crt_subcategories.objects.annotate(tmp=tmp)
            # categories = tbl_crt_subcategories.objects.annotate(Count('tbl_creativeitems_mst'),filter=Q(tbl_creativeitems_mst__crt_sub_category=3))
            # print(categories[0].tmp)  
            # print(subCrtCats)
            parentCat=get_object_or_404(tbl_crt_categories,pk=id)

            if subCrtCats!= None:
                return render(request,template,{"subCrtCats":subCrtCats,"mainCat":crtMainCats,"parentCat":parentCat, "dispSubCat":True})
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
                            
        
        return render(request,template,{"dispSubCat":False,"mainCat":crtMainCats,"form":mainCrtCat,"mainCrtCnt":zip(crtMainCats, mainCrtCnt)})
    else:
        return redirect('CustomAdmin:login')



def creativeitems(request):
    if request.user.is_superuser:
        template = 'custom-admin/products/creativeitems.html'
        items = tbl_creativeitems_mst.objects.all()
        return render(request,template,{"dispSubCat":False, "items": items})
    else:
        return redirect('CustomAdmin:login')

############################################
### SCRAP ###
def scrapCat(request,id=None,action=None):
   # print("SCRAPCAT FUNC")
    if request.user.is_superuser:   
        scpMainCats=MainScrapCategory.objects.all().order_by("scp_category_name")
        template = 'custom-admin/products/scrapcategory.html'
        # print("OUT")
        mainScpCnt = SubScrapCategory.objects.values("scp_category__scp_category_name").annotate(ScpCnt=Count('tbl_scrapitems'))

        if id != None and action==None :
            # print("DD1")
            subScpCats=SubScrapCategory.objects.filter(scp_category_id=id).order_by("scp_sub_category_name")
            parentCat=get_object_or_404(MainScrapCategory,pk=id)
                
            if subScpCats!= None:
                return render(request,template,{"subScpCats":subScpCats,"mainCat":scpMainCats,"parentCat":parentCat, "dispSubCat":True ,"mainScpCnt":zip(scpMainCats, mainScpCnt)})
            else:
                return render(request,template,{"subScpCats":subScpCats,"mainCat":scpMainCats, "parentCat":parentCat,"dispSubCat":True ,"mainScpCnt":zip(scpMainCats, mainScpCnt)})

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
                    err=mainScpCat.errors.get_json_data(escape_html=True)
                    err=err['__all__'][0]['message']
                    return JsonResponse({"saved":False,"message":err}) 
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
                    err=newSubScpCat.errors.get_json_data(escape_html=True)
                    err=err['__all__'][0]['message']
                    return JsonResponse({"saved":False,"message":err}) 
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
                    err=editMainScpCat.errors.get_json_data(escape_html=True)
                    err=err['__all__'][0]['message']
                    return JsonResponse({"saved":False,"message":err}) 
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
                    err=editSubScpCat.errors.get_json_data(escape_html=True)
                    err=err['__all__'][0]['message']
                    return JsonResponse({"saved":False,"message":err}) 
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
        return render(request,template,{"dispSubCat":False,"mainCat":scpMainCats,"mainScpCnt":zip(scpMainCats, mainScpCnt)})

    else:
        return redirect('CustomAdmin:login')

        
def scrapitems(request):
    if request.user.is_superuser:    
        template = 'custom-admin/products/scrapitems.html'
        # items = tbl_scrapitems.objects.order_by('scp_created_on')[::-1]
        items = tbl_scrapitems.objects.all()

        return render(request, template, {"items": items})
    else:
        return redirect('CustomAdmin:login')

####### ORDERS RELATED #######
def allorders(request):
    if request.user.is_superuser:    
        template = 'custom-admin/allorders.html'

        if request.method == "POST":
            try:
                id = request.POST.get('ordId')
                currentStatus = request.POST.get('currentStatus')
                orderObj = tbl_orders_mst.objects.get(order_id=id)
                orderObj.delivery_status = currentStatus
                orderObj.save()
            except Exception as e:
                messages.error(request, "Something went wrong." + str(e))

        orders = tbl_orders_mst.objects.all()

        return render(request,template,{'orders':orders})
    else:
        return redirect('CustomAdmin:login')


def orderdetails(request,id):
    if request.user.is_superuser:

        if request.method == "POST":
            detailId = request.POST.get('detailId')
            currentStatus = request.POST.get('currentStatus')
            detailObj = tbl_orders_details.objects.get(order_details_id=detailId)
            detailObj.item_status = currentStatus
            detailObj.save()

        template = 'custom-admin/orderdetails.html'
        order = tbl_orders_mst.objects.get(order_id = id)
        orderDetails = tbl_orders_details.objects.filter(order_id = id) #.annotate(totalPrice=Sum(F('crt_item_qty') * F('unit_price'),output_field=models.DecimalField()))
        totalPrice = tbl_orders_details.objects.filter(order_id = id).aggregate(tot = Sum(F('crt_item_qty') * F('unit_price'),output_field=models.DecimalField()))
        commission = float(totalPrice['tot']) * 0.2
        # print(totalPrice)

        try:
            payment = Payment.objects.get(order)
            print(payment)
        except:
            payment = None
        context = {
            "order": order,
            "orderDetails": orderDetails,
            "payment": payment,
            "totalPrice": totalPrice,
            "commission": commission
        }

        return render(request,template,context)
    else:
        return redirect('CustomAdmin:login')

def allorderdetails(request,action='delivered'):
    
    if request.user.is_superuser:  
        #print(action)
        if action == 'delivered':
            title = "Delivered Orders"
            details = tbl_orders_details.objects.filter(item_status = 2)
        elif action == 'returned':
            title = "Returned Orders"
            details = tbl_orders_details.objects.filter(item_status=5)
        elif action == 'processing':
            title = "Processing Orders"
            details = tbl_orders_details.objects.filter(item_status=1)
        elif action == 'canceled':
            title = "Cancelled Orders"
            details = tbl_orders_details.objects.filter(item_status=3)

        context = {
            "title": title,
            "details": details
        }
        template = 'custom-admin/allorderdetails.html'
        return render(request,template, context)
    else:
        return redirect('CustomAdmin:login')

#######    PAYMENT     #######

def payment(request):
    if request.user.is_superuser:    
        template = 'custom-admin/payment.html'
        payments = Payment.objects.all()

        return render(request, template, {"payments": payments})
    # elif request.session.post('post'):

    else:
        return redirect('CustomAdmin:login')
####### BADGES RELATED #######
def badges(request):
    if request.user.is_superuser:    
        template = 'custom-admin/manage-badges.html'
        badges=Badges.objects.all()
        badgeEntries=BadgeEntries.objects.all()
        context={
            'badges':badges,
            'badgeEntries':badgeEntries,
        }
        return render(request,template,context)

    else:
        return redirect('CustomAdmin:login')

@login_required
def assignBadges(request):
    if request.user.is_superuser:  

        msg=""
        if request.method=='POST' and request.is_ajax():

            email=request.POST.get('email')
            badge_id=request.POST.get('badge_id',None)
            
            isEmailExist = User.objects.filter(email=email,is_superuser=False,is_active=True).exists()
            if not isEmailExist and (badge_id=="" or badge_id is None):
                msg={
                    "email":"Given email does not exists or user account is disabled.",
                    "badge":"Please select the badge."
                }
                return JsonResponse({"errors":msg})
            elif not isEmailExist:
                msg={
                    "email":"Given email does not exists or user account is disabled.",
                }

                return JsonResponse({"errors":msg})
            elif badge_id=="" or badge_id is None:
                msg={
                    "badge":"Please select the badge."
                }
                return JsonResponse({"errors":msg})
           
            else:
                usr=User.objects.get(email=email)
                badge = Badges.objects.get(badge_id=badge_id)
                isAlreadyAsssigned = BadgeEntries.objects.filter(badge=badge,user=usr).exists()
                if isAlreadyAsssigned:
                    # messages.success(request,"Badge already assigned to the user.")
                    return JsonResponse({"errors":"assigned"})
                    

                assignBadge=BadgeEntries.objects.create(badge=badge,user=usr)
    
                assignBadge.save()
                messages.success(request,"Badge assigned successfully.")
                
                return JsonResponse({"errors":False})
            
    else:
        raise PermissionDenied
    
def addBadges(request):
    if request.is_ajax and request.method=="POST":
        # print("How's The Code",request.POST)
        name=request.POST.get("badge_name",None)
        if name is not None or name!=" ":
            if bool(re.match("^[a-zA-Z\s]+$",name)):
                isBadge = Badges.objects.filter(badge_name__iexact=name).exists()
                if isBadge:
                    return JsonResponse({"success":False,"msg":"Badge already exist!!"})

                badge=Badges.objects.create(badge_name=name)
                badge.save()
                return JsonResponse({"success":True})
            else:
                return JsonResponse({"success":False,"msg":"Only alphabets are allowed."})

        else:
            return JsonResponse({"success":False,"msg":"You need to write something"})
    else:
        raise PermissionDenied

def delBadge(request):
    if request.is_ajax and request.method=="POST":
        # print("How's The Code",request.POST)
        badge_id=request.POST.get("badge_id",None)
        
        if badge_id:
            isBadge = Badges.objects.filter(badge_id=badge_id).exists()
            if not isBadge:
                return JsonResponse({"success":False,"msg":"Some Error occured!!"})

            badge=Badges.objects.get(badge_id=badge_id)
            badge.delete()

            return JsonResponse({"success":True})
        else:
            return JsonResponse({"success":False,"msg":"Some Error occured!"})
    else:
        raise PermissionDenied

def removeAssignedBadge(request):
    if request.is_ajax and request.method=="POST":
        # print("How's The Code",request.POST)
        entry_id=request.POST.get("entry_id",None)
        
        if entry_id:
            isBadge = BadgeEntries.objects.filter(entry_id=entry_id).exists()
            if not isBadge:
                return JsonResponse({"success":False,"msg":"Some Error occured!!"})

            badge=BadgeEntries.objects.get(entry_id=entry_id)
            badge.delete()

            return JsonResponse({"success":True})
        else:
            return JsonResponse({"success":False,"msg":"Some Error occured!"})
    else:
        raise PermissionDenied
####### QUERIES RELATED #######
def queries(request,qryid=None):
    if request.user.is_superuser:    
        template = 'custom-admin/queries/queries.html'
        Qry = Query.objects.all()

        if request.method == "POST" and qryid is not None:
            
            status  = request.POST.get("query_status","")
            try:
                qry = Query.objects.get(query_id=qryid)
            except Query.DoesNotExist:
                pass
            else:
                qry.query_status = status
                qry.save()

        context={
            "queries":Qry,
        }
        return render(request,template,context)

    else:
        return redirect('CustomAdmin:login')    

def issues(request,issid=None):
    if request.user.is_superuser:    
        template = 'custom-admin/queries/issues.html'
        title = "Reported Creative Items"
        issueType=1
        columnName="Item SKU"
        issues=Issues.objects.filter(issue_type=1)
        if request.method=="POST" and issid is None:
            issueType=request.POST.get("issueType")

            if issueType == '1':
                title = "Reported Creative Items"
                issueType=1
                columnName="Item SKU"
                issues=Issues.objects.filter(issue_type=1)
            elif issueType == '2' :
                title= "Reported Scrap Items"
                issueType=2
                columnName="Item SKU"
                issues=Issues.objects.filter(issue_type=2)
            elif issueType == '3' :
                title =  "Reported Users Items"
                issueType=3
                columnName="Reported Username"
                issues=Issues.objects.filter(issue_type=3)

            # elif issueType == '4':
            #     title = "Order Issues" 
            #     issueType=4    
            #     columnName="Oreder Detail ID"  
        
        if request.method == "POST" and issid is not None:
            status  = request.POST.get("issue_status","")
            try:
                iss = Issues.objects.get(issue_id=issid)
            except Query.DoesNotExist:
                pass
            else:
                iss.issue_status = status
                iss.save()
        
        context = {
            "title":title,
            "issueType":issueType,
            "columnName":columnName,
            "issues":issues,
            
        }
        return render(request,template,context)

    else:
        return redirect('CustomAdmin:login')
####### SEND EMAIL RELATED #######
@login_required
def sendmail(request):
    if request.user.is_superuser:    
        template = 'custom-admin/sendmail/sendmail.html'
        registerEmails = User.objects.filter(is_active=True,is_superuser=False)
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
            Id = request.POST.get('Id', '')
            

            if typeFor == "user":
                #print(email.split(","),subject,emailmessage)
                try:
                    usr=User.objects.get(email=email)
                    usr.is_active=False
                    usr.save()
                    
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

                    if request.POST.get("item")=='crt':                    
                        item=tbl_creativeitems_mst.objects.get(crt_item_id=Id)
                        item.crt_item_status="INAPPROPRIATE"
                        item.save()
                    elif request.POST.get("item")=='scp':
                        item=tbl_scrapitems.objects.get(scp_item_id=Id)
                        print(item)
                        item.scp_item_status="INAPPROPRIATE"
                        item.save()

                    emailList=item.user.email
                    current_site = get_current_site(request)
                    mail_subject = "Your Product is disabled"
                    message = render_to_string('common/email.html', {
                        'message':str("\n")+emailmessage,
                        'type':"product",
                        'item':item,
                    })
                    to_email = email
                    email = EmailMessage(
                                mail_subject, message, to=[emailList,]
                    )
                    email.send()
                    
                except Exception as e:
                    return redirect({"send":True,"msg":str(e)})           
                else:
                    return JsonResponse({"send":True,"msg":"Mail Sent"})
            
                    
            #return JsonResponse({"send":True,"msg":"Mail Sent"})


        context={
            "emailList":registerEmails
        }
        return render(request,template,context)
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

def sendVerifiedMail(typeFor,profile,verified):    
    if typeFor == "verifiedUser":
        print(verified)
        try:
            if verified:
                emailmessage="You have been verified now you can sell creative item."\
                    + "http://127.0.0.1:8000/accounts/dashboard/product/creative/"
                emailmessage+="\n\nThank You."
                mail_subject = "Verification Done!!"
            
            else:
                emailmessage="Your verification request is rejected."+"\nFor more details contact us."
                emailmessage+="\n\nThank You."
                mail_subject = "Verification Done!!"

            message = render_to_string('common/email.html', {
                'message':str("\n")+emailmessage,
                'user':User.objects.get(user_id=profile.user_id),
                'type':"verifiedUser",
                "verified":verified
            })


            to_email = profile.user.email
            email = EmailMessage(
                        mail_subject, message, to=[to_email,]
            )
            email.send()
        except Exception as e:
            
            print("MAIL EXCEPTION : "+str(e))
            return False     
        else:
            return True
######################################################
# def loadSubCrtCats(request,id=None):
#     if request.user.is_superuser:
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