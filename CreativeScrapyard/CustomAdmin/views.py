from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse,HttpResponse
import mimetypes,os
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from wsgiref.util import FileWrapper
from django.utils.encoding import smart_str

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
def creativeCat(request):
    if request.session.get('admin'):    
        template = 'custom-admin/products/creativecategory.html'
        return render(request,template)
    else:
        return redirect('CustomAdmin:login')

def creativeitems(request):
    if request.session.get('admin'):    
        template = 'custom-admin/products/creativeitems.html'
        return render(request,template)
    else:
        return redirect('CustomAdmin:login')
### SCRAP ###
def scrapCat(request):
    if request.session.get('admin'):    
        template = 'custom-admin/products/scrapcategory.html'
        return render(request,template)
    else:
        return redirect('CustomAdmin:login')
def scrapitems(request):
    if request.session.get('admin'):    
        template = 'custom-admin/products/scrapitems.html'
        return render(request,template)
    else:
        return redirect('CustomAdmin:login')

####### ORDERS RELATED #######

####### BADGES RELATED #######
def badges(request):
    template = 'custom-admin/manage-badges.html'
    return render(request,template)


