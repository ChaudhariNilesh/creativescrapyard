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
from .forms import MainCreativeCategoryForm, SubCreativeCategoryForm, MainScrapCategoryForm, SubScrapCategoryForm
from django.http import HttpResponseNotFound
from django.core.exceptions import PermissionDenied
from django.http import Http404
from django.core import serializers
####### AUTH RELATED #######
def login(request):
    template = 'custom-admin/login.html'
    if request.method == 'POST':
        user = request.POST['username']
        pwd = request.POST['password']
        if user=='admin' and pwd=='admin':
            request.session['admin'] = user
            return redirect('CustomAdmin:adminindex')
    return render(request,template)

def adminindex(request):
    if request.session.get('admin'):
        template='custom-admin/admin-dashboard.html'
        
        return render(request,template)
    else:
        return redirect('CustomAdmin:login')

def adminAccount(request):
    if request.session.get('admin'): 
        template = 'custom-admin/account-settings/admin-account.html'
        return render(request,template)
    else:
        return redirect('CustomAdmin:login')
        
def changePassword(request):
    if request.session.get('admin'):    
        template = 'custom-admin/account-settings/change-password.html'
        return render(request,template)
    else:
        return redirect('CustomAdmin:login')

def logout(request):
    if request.session.get('admin') != None:
        request.session.delete()
        return redirect('CustomAdmin:login')
    else:
        return redirect('CustomAdmin:login')



####### USERS RELATED #######

def users(request):
    if request.session.get('admin'):    
        template = 'custom-admin/users/users.html'
        return render(request,template)
    else:
        return redirect('CustomAdmin:login')

def buyers(request):
    if request.session.get('admin'): 
        template = 'custom-admin/users/buyers.html'
        return render(request,template)
    else:
        return redirect('CustomAdmin:login')

def sellers(request):
    if request.session.get('admin'): 
        template = 'custom-admin/users/sellers.html'
        return render(request,template)
    else:
        return redirect('CustomAdmin:login')

def verifyusers(request):
    if request.session.get('admin'): 
        template = 'custom-admin/users/verify-users.html'
        return render(request,template)
    else:
        return redirect('CustomAdmin:login')

####### AJAX VERIFY USERS #######
def viewDets(request):
    if request.session.get('admin'): 
        data={"bankName":"SBI","bankifscCode":"ABC0123","accNo":"1234567890","accName":"Dummy Dummy",\
            "panNo":"ABCD123456","panName":"Dummy Dummy"}
        return JsonResponse(data)
    else:
        return redirect('CustomAdmin:login')

def docuDownload(request):
    if request.session.get('admin'): 
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
    if request.session.get('admin'): 
        data={"is_verified":True}
        return JsonResponse(data)
    else:
        return redirect('CustomAdmin:login')

####### PRODUCTS RELATED #######
### CREATIVE ###

def creativeCat(request,id=None,action=None):
    if request.session.get('admin'):
        crtMainCats=tbl_crt_categories.objects.all()
        template = 'custom-admin/products/creativecategory.html' 
        mainCrtCat=MainCreativeCategoryForm()
        if id != None and action==None :
            #print("DD1")
            subCrtCats=tbl_crt_subcategories.objects.filter(crt_category_id=id)
            parentCat=get_object_or_404(tbl_crt_categories,pk=id)
                
            if subCrtCats!= None:
                return render(request,template,{"subCrtCats":subCrtCats,"mainCat":crtMainCats,"parentCat":parentCat, "dispSubCat":True })
            else:
                return render(request,template,{"subCrtCats":subCrtCats,"mainCat":crtMainCats, "parentCat":parentCat,"dispSubCat":True })

        elif action=="addMain":
           # print("DD2")
            if request.method=="POST" and request.is_ajax():
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
                    err=err['__all__'][0]['message']
                    # print(err)
                    
                    return JsonResponse({"saved":False,"message":err})
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
                    return JsonResponse({"saved":False,"message":"Invalid Data!!"})
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
                    return JsonResponse({"updated":False,"message":"Invalid Data!!"})
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
                    return JsonResponse({"updated":False,"message":"Invalid Data!!"})
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
                            
        #print(mainCrtCat)
        return render(request,template,{"dispSubCat":False,"mainCat":crtMainCats,"form":mainCrtCat})
    else:
        return redirect('CustomAdmin:login')



def creativeitems(request):
    if request.session.get('admin'):    
        template = 'custom-admin/products/creativeitems.html'
        return render(request,template,{"dispSubCat":False})
    else:
        return redirect('CustomAdmin:login')

############################################
### SCRAP ###
def scrapCat(request,id=None,action=None):
   # print("SCRAPCAT FUNC")
    if request.session.get('admin'):   
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
    if request.session.get('admin'):    
        template = 'custom-admin/products/scrapitems.html'
        return render(request,template)
    else:
        return redirect('CustomAdmin:login')

####### ORDERS RELATED #######
def allorders(request):
    if request.session.get('admin'):    
        template = 'custom-admin/allorders.html'
        return render(request,template)
    else:
        return redirect('CustomAdmin:login')

def orderdetails(request,id):
    if request.session.get('admin'):    
        template = 'custom-admin/orderdetails.html'
        return render(request,template)
    else:
        return redirect('CustomAdmin:login')

####### BADGES RELATED #######
def badges(request):
    template = 'custom-admin/manage-badges.html'
    return render(request,template)

####### QUERIES RELATED #######
def queries(request):
    template = 'custom-admin/queries/queries.html'
    return render(request,template)

####### SEND EMAIL RELATED #######
def sendmail(request):
    template = 'custom-admin/sendmail/sendmail.html'
    if request.method == "POST":
        email = request.POST.get('email', '')
        subject = request.POST.get('subject', '')
        message = request.POST.get('message', '')
        print(email.split(","),subject,message)
    return render(request,template)




######################################################
# def loadSubCrtCats(request,id=None):
#     if request.session.get('admin'):
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