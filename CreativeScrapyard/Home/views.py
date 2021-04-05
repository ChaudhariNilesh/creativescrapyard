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
    crt_products=tbl_creativeitems_mst.objects.filter(crt_item_status="ACTIVE")
    # ids=crt_products.values_list('crt_item_id',flat=True)
    # r_ids = random.sample(list(ids), 12)
#   crt_products=all_products.filter(crt_item_id__in=r_ids)
    scp_products=tbl_scrapitems.objects.filter(scp_item_status="ACTIVE")
    # ids=scp_products.values_list('scp_item_id',flat=True)
    # r_ids = random.sample(list(ids), 0)
    # scp_products=all_products.filter(scp_item_id__in=r_ids)
    return render(request,template,{'is_home':True,'crt_products':crt_products,'scp_products':scp_products})

def creativestore(request,type="all",id=None,products=None):
    # print(tmp,products)
    min_value=100
    max_value=1000
    template="Home/creativestore.html"
    subcategory=None
    parentcategory=None
    search=""
    
    categories=tbl_crt_categories.objects.all()
    if type=="s":
        
        subcategory=get_object_or_404(tbl_crt_subcategories,crt_sub_category_id=id)
        parentcategory=subcategory.crt_category
        products = tbl_creativeitems_mst.objects.filter(crt_sub_category=id,crt_item_status="ACTIVE")

        sortBy = request.GET.get('sort','relv')
        products,sort=sortByFn(sortBy,products)

        if request.method == "POST":
            products,min_value,max_value,search = FilterNSrch(request.POST,products)
   
    elif type=="m":
        
        subcategories=tbl_crt_subcategories.objects.filter(crt_category=id)
        parentcategory=get_object_or_404(tbl_crt_categories.objects,crt_category_id=id)
        products=tbl_creativeitems_mst.objects.filter(crt_sub_category__in=subcategories,crt_item_status="ACTIVE")
        
        sortBy = request.GET.get('sort','relv')
        products,sort=sortByFn(sortBy,products)

        if request.method == "POST":
            products,min_value,max_value,search = FilterNSrch(request.POST,products)
   
    elif type=="all":

        products = tbl_creativeitems_mst.objects.filter(crt_item_status="ACTIVE")

        sortBy = request.GET.get('sort','relv') 
        products,sort=sortByFn(sortBy,products)
        
        if request.method == "POST" :
            products,min_value,max_value,search = FilterNSrch(request.POST,products)

    context={
        'products':products,
        'is_creative':True,
        'categories':creativeCategories(),
        'sub_category':subcategory,
        'parent_category':parentcategory,
        'type':type,
        'sort':sort,
        'min_value':min_value,
        'max_value':max_value,
        'search':search,
        
        }
    
    return render(request,template,context)  

def sortByFn(sort,products):
    if sort=="lh":
        products=products.order_by("crt_item_price")
        sort="Low To High Price"

    elif sort=="hl":
        products=products.order_by("-crt_item_price")
        sort="High To Low Price"

    elif sort=="mr":
        products=products.order_by("-crt_created_on")
        sort="Most Recent"

    elif sort=="alpha":
        products=products.order_by("crt_item_name")
        sort="Alphabetic"   

    elif sort=="top":
        products=products.order_by("-user__profile__user_rating")
        sort="Top Review Artist"
   
    elif sort=="relv":
        sort="Relevance"
        products = products.filter(crt_item_status="ACTIVE")    
    
    return products,sort


def FilterNSrch(postDate,prdObj):

    search=postDate.get('search',"")
    min_value = postDate.get('min_value',100)
    max_value = postDate.get('max_value',1000)
    
    if search:
        productSrch=prdObj.filter(crt_item_name__icontains=search)
        

        if min_value and max_value:
            products=productSrch.filter(crt_item_price__range=(min_value,max_value))
          
    
    elif not search :
            products=prdObj.filter(crt_item_price__range=(min_value,max_value))

    return products,min_value,max_value,search


# def priceFilter(min_value,max_value,prdObj):
    
#     products=prdObj.filter(crt_item_price__range=(min_value,max_value))

#     return products,min_value,max_value

# def priceFilter(postData,prdObj):
    
#     products=prdObj.filter(crt_item_price__range=(postData.get('min_value'),postData.get('max_value')))
#     min_value=postData.get('min_value')
#     max_value=postData.get('max_value')
#     return products,min_value,max_value

def scrapyard(request,type="all",id=None,sort=None):
    template="Home/scrapyard.html"
    min_value=100
    max_value=1000
    products=None
    # if request.POST:
    #     products=tbl_scrapitems.objects.filter(scp_item_price__range=(request.POST.get('min_value'),request.POST.get('max_value')))
    #     min_value=request.POST.get('min_value')
    #     max_value=request.POST.get('max_value')

    subcategory=None
    parentcategory=None
    search=""
    categories=MainScrapCategory.objects.all()
    if type=="s":
        subcategory=get_object_or_404(SubScrapCategory,scp_sub_category_id=id)
        parentcategory=subcategory.scp_category
        products = tbl_scrapitems.objects.filter(scp_sub_category_id=id,scp_item_status="ACTIVE")
       
        if request.method == "POST":
            products,min_value,max_value,search = FilterNSrch(request.POST,products)
   
    elif type=="m":
        subcategories=SubScrapCategory.objects.filter(scp_category=id)
        parentcategory=get_object_or_404(MainScrapCategory.objects,scp_category_id=id)
        products=tbl_scrapitems.objects.filter(scp_sub_category__in=subcategories,scp_item_status="ACTIVE")

        if request.method == "POST":
            products,min_value,max_value,search = FilterNSrch(request.POST,products)
   
    elif type=="all":
        products = tbl_scrapitems.objects.filter(scp_item_status="ACTIVE")
        
        if request.method == "POST" :
            products,min_value,max_value,search = FilterNSrch(request.POST,products)
            

    if sort is not None:
        
        if sort=="lh":
            products=products.order_by("scp_item_price")
            sort="Low To High Price"


        elif sort=="hl":
            products=products.order_by("-scp_item_price")
            sort="High To Low Price"

        elif sort=="mr":
            products=products.order_by("scp_created_on")
            sort="Most Recent"

        elif sort=="alpha":
            products=products.order_by("scp_item_name")
            sort="Alphabetic"   

        elif sort=="top":
            products=products.order_by("-user__profile__user_rating")
            sort="Top Review Artist"     
        
        else:
            products = tbl_scrapitems.objects.filter(scp_item_status="ACTIVE")

    context={
        'products':products,
        'is_scrap':True,
        'categories':scrapCategories(),
        'sub_category':subcategory,
        'parent_category':parentcategory,
        'type':type,
        # 'sort':sort,
        'min_value':min_value,
        'max_value':max_value,
        'search':search,
        }
    return render(request,template,context)    

def creativeCategories():
    categories=tbl_crt_categories.objects.all()
    return categories

def scrapCategories():
    categories=MainScrapCategory.objects.all()
    return categories

def achievers(request):
    template="achievers.html"
    
    aotm_badge=Badges.objects.filter(badge_name="Artist Of The Month").exists()
    bsa_badge=Badges.objects.filter(badge_name="Best Seller Artist").exists()
    hw_badge=Badges.objects.filter(badge_name="Heart Winner").exists()
    cotm_badge=Badges.objects.filter(badge_name="Creator Of The Month").exists()
    
    if aotm_badge:
        aotm_badge=Badges.objects.get(badge_name="Artist Of The Month")
        aotm_user=BadgeEntries.objects.filter(badge=aotm_badge)
    else:
        aotm_user=None
    
    if bsa_badge:
        bsa_badge=Badges.objects.get(badge_name="Best Seller Artist")
        bsa_user=BadgeEntries.objects.filter(badge=bsa_badge)
    else:
        bsa_user=None

    if hw_badge:
        hw_badge=Badges.objects.get(badge_name="Heart Winner")    
        hw_user=BadgeEntries.objects.filter(badge=hw_badge)
    else:
        hw_user=None                

    if cotm_badge:
        cotm_badge=Badges.objects.get(badge_name="Creator Of The Month")
        cotm_user=BadgeEntries.objects.filter(badge=cotm_badge)
    else:
        cotm_user=None
    
    # try:
        
        # aotm_badge=Badges.objects.get(badge_name="Artist Of The Month")
        # bsa_badge=Badges.objects.get(badge_name="Best Seller Artist")
        # hw_badge=Badges.objects.get(badge_name="Heart Winner")    
        # # cotm_badge=Badges.objects.get(badge_name="Creator Of The Month")

        
        # aotm_user=BadgeEntries.objects.filter(badge=aotm_badge)
        # bsa_user=BadgeEntries.objects.filter(badge=bsa_badge)
        # hw_user=BadgeEntries.objects.filter(badge=hw_badge)        
        # cotm_user=BadgeEntries.objects.filter(badge=cotm_badge)
        
    # except:
    #     aotm_user=None
    #     bsa_user=None
    #     hw_user=None
    #     cotm_user=None
    
    context={
        'is_creative':True,
        'categories':creativeCategories(),
        'aotm_user':aotm_user,
        'bsa_user':bsa_user,
        'hw_user':hw_user,
        'cotm_user':cotm_user,

    }
    return render(request,template,context)    

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
        'categories':creativeCategories(),
    }

    #print(context)

    return render(request,template,context)


def aboutus(request):
    template="about-us.html"
    return render(request,template,{'is_creative':True,'categories':creativeCategories()})

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

    return render(request,template,{'is_scrap':True,'categories':creativeCategories()})         
