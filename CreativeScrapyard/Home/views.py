from django.shortcuts import render,get_object_or_404
from django.shortcuts import render,redirect
from .forms import QueryForm
from .models import *
from Home.validate import *
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from Authentication.models import *
from CustomAdmin.models import *
from Items.models import *
from django.template.loader import render_to_string
from django.http import JsonResponse,HttpResponse
# Create your views here.
def home(request):
    template="Home/index.html"
    #print(request.user)
    return render(request,template,{'is_home':True})

def creativestore(request,type="all",id=None,products=None):
    # print(tmp,products)
    min_value=100
    max_value=1000
    template="Home/creativestore.html"
    subcategory=None
    parentcategory=None
    
    categories=tbl_crt_categories.objects.all()
    if type=="s":
        subcategory=get_object_or_404(tbl_crt_subcategories,crt_sub_category_id=id)
        parentcategory=subcategory.crt_category
        products = tbl_creativeitems_mst.objects.filter(crt_sub_category=id)
       
        if request.POST:
            products,min_value,max_value=priceFilter(request.POST,products)
   
    elif type=="m":
        subcategories=tbl_crt_subcategories.objects.filter(crt_category=id)
        parentcategory=get_object_or_404(tbl_crt_categories.objects,crt_category_id=id)
        products=tbl_creativeitems_mst.objects.filter(crt_sub_category__in=subcategories)

        if request.POST:
            products,min_value,max_value=priceFilter(request.POST,products)
   
    elif type=="all":
        products = tbl_creativeitems_mst.objects.all()
        search=request.POST.get('search')
        if request.POST and request.POST.get('search') is None :
            products,min_value,max_value=priceFilter(request.POST,products)

        if request.POST and request.POST.get('search') is not None:
            
            products=tbl_creativeitems_mst.objects.filter(crt_item_name__icontains=request.POST.get('search'))
            
            if request.POST and request.POST.get('search') is None:
                products,min_value,max_value=priceFilter(request.POST,products)
            

    context={
        'products':products,
        'is_creative':True,
        'categories':categories,
        'sub_category':subcategory,
        'parent_category':parentcategory,
        'type':type,
        'min_value':min_value,
        'max_value':max_value,
        }
    
    return render(request,template,context)    

def priceFilter(postData,prdObj):
    products=prdObj.filter(crt_item_price__range=(postData.get('min_value'),postData.get('max_value')))
    min_value=postData.get('min_value')
    max_value=postData.get('max_value')
    return products,min_value,max_value

def scrapyard(request):
    template="Home/scrapyard.html"
    products = tbl_scrapitems.objects.all()
    min_value=100
    max_value=1000
    if request.POST:
        products=tbl_scrapitems.objects.filter(scp_item_price__range=(request.POST.get('min_value'),request.POST.get('max_value')))
        min_value=request.POST.get('min_value')
        max_value=request.POST.get('max_value')

    context={'products':products,'is_scrap':True,'min_value':min_value,
        'max_value':max_value,}

    return render(request,template,context)    

def achievers(request):
    template="achievers.html"
    return render(request,template,{'is_creative':True})    

def contactus(request):
    template="contact-us.html"
    formData = QueryForm()
    errorData={}
    if request.method == 'POST':
        
        formData = QueryForm(request.POST or None)
      
        email = request.POST.get('email','')
        first_name = request.POST.get('first_name','')
        last_name = request.POST.get('last_name','')
        query_subject = request.POST.get('query_subject','')
        query_message = request.POST.get('query_message','')


        errorData = validate(email=email,fname=first_name,lname=last_name,sub=query_subject,msg=query_message,chkTakenEmail=False,chkTakenUsrname=False)
        #print(errorData)
       
        if not errorData['errors']:
            QryModel=Query(first_name=first_name,last_name=last_name,email=email,query_subject=query_subject,\
                query_message=query_message)
            try:
                QryModel.save()
                messages.success(request, 'Your Query is submitted sucessfully!')  
                formData=QueryForm()
                errorData.clear()
                return redirect("Home:contactus")
            except:
                messages.error(request, 'Some error occured try after sometime.')
        else:
            messages.warning(request, 'Please correct the error below.')
            #'Please correct the error below.')
            # context['form']=formData
        # else:
            # return redirect("Home:contactus")

    
    context={
        "is_creative":True,
        "form":formData,
        "errorData":errorData,
    }

    #print(context)

    return render(request,template,context)


def aboutus(request):
    template="about-us.html"
    return render(request,template,{'is_creative':True})

def sendContactDetails(request):
    
    template="Home/scrapyard.html"
    
    if request.is_ajax() and request.method == "POST":
        if request.user.is_authenticated:
            
            try:                
                # current_site = get_current_site(request)
                mail_subject = "Buyer showed interest in your scrap item"
                #get user related to scrap
                sellerEmail = request.POST.get("seller","")
                seller = User.objects.get(email__iexact=sellerEmail)
                if seller==request.user:
                    return JsonResponse({"send":False,"msg":"You can't contact yourself!!","auth":True})
                # print(seller.email)
                message = render_to_string('common/email.html', {
                    'message':"shared mail id with you. Please contact him/her from this email.",
                    'user':request.user,
                    'seller':seller, # here get the product related email
                    'type':"contactuser"
                    
                })
                to_email = seller.email
                email = EmailMessage(
                            mail_subject, message, to=[to_email]
                )
                email.send()

            except Exception as e:
                return redirect({"send":True,"msg":str(e),"auth":True})           
            else:
                return JsonResponse({"send":True,"msg":"Mail Sent","auth":True})
        else:
            return JsonResponse({"send":False,"msg":"","auth":False})

    else:
        raise PermissionDenied

    return render(request,template,{'is_scrap':True})         
