
from django.db.models.query import InstanceCheckMeta
from django.shortcuts import render, redirect,HttpResponse,get_object_or_404
from .models import*
from .forms import *
from CustomAdmin.models import *
from Home.views import creativeCategories,scrapCategories
from Items.forms import *
from Items.models import *
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Count,Sum,F,Q
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
from django.core.exceptions import PermissionDenied
import requests,random,string
from Order.models import *
from Payments.models import *


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
            userProfile = Profile(user_id=userSignUp.user_id,user_gender=gender)
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
        #login(request, user)
        return render(request,template,{"activated":True})
        #return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    else:
        return render(request,template,{"activated":False})


def logout(request):
    
    if (request.session.get('user') != None):
        # print("exist")
        request.session.delete()
        return redirect('Home:home')
    else:
        return redirect('Authentication:login')


def profile(request,id):
    template = "account/profile.html"
    artist_details=get_object_or_404(User,user_id=id)
    try:
        defaultAddress = Address.objects.get(user_id=id,is_default=True)
    except:
        defaultAddress=None
    
    crt_products = tbl_creativeitems_mst.objects.filter(user=id)
    # print(crt_products)
    scp_products = tbl_scrapitems.objects.filter(user=id)
    reviews=Reviews.objects.filter(crt_item__in = crt_products,crt_item__user__user_id=id).annotate(reviewCnt=Count("user_id"))
    reviewCnt = reviews.count()
    # print(reviews.values("reviewCnt"))
    # print(reviewCnt)

    badges=BadgeEntries.objects.filter(user=id)
    context={
        "is_creative":True,
        "artist":artist_details,
        "artist_address":defaultAddress,
        "crt_products":crt_products,
        "scp_products":scp_products,
        "reviews":reviews,
        'categories':creativeCategories(),
        "badges":badges,
        "reviewCnt":reviewCnt
    }
    return render(request, template, context)


def creative_items(request):
    p = Profile.objects.get(user=request.user)
    if not p.is_verified :
        return HttpResponse("Page not Found.")
    products=tbl_creativeitems_mst.objects.filter(user=request.user)
    template = "account/dashboard/creative-items.html"

    if request.method == "POST":
        try:
            id = request.POST.get('itemId')
            itemStatus = request.POST.get('statusSelect')
            itemObj = tbl_creativeitems_mst.objects.get(crt_item_id=id)
            itemObj.crt_item_status = itemStatus
            itemObj.save()
        except Exception as e:
            messages.error(request,"Something went wrong." + str(e))

    context={
        "myProducts":products
    }
    return render(request, template,context)    


def scrap_items(request):
    template = "account/dashboard/scrap-items.html"

    if request.method == "POST":
        try:
            id = request.POST.get('itemId')
            itemStatus = request.POST.get('statusSelect')
            itemObj = tbl_scrapitems.objects.get(scp_item_id=id, user=request.user)
            itemObj.scp_item_status = itemStatus
           
            itemObj.scp_item_qty = 0
            itemObj.save()

        except Exception as e:
            messages.error(request,"Something went wrong." + str(e))

    products = tbl_scrapitems.objects.filter(user=request.user)
    context={
        "myProducts":products
    }
    return render(request, template,context)


def add_creative_product(request):
    context={}

    address = Address.objects.filter(user = request.user)
    # print(address)
    if Address.objects.filter(user = request.user):
        address = True
    else:
        address = False
    # print(address)
    template = "account/dashboard/add-product/add-product.html"
    crtCategory = tbl_crt_categories.objects.all()

    context["check_for_address"]= address
    context['crtCategory']=crtCategory

    if request.method == "POST":
        productDetail = tbl_creativeitems_mst_form(request.POST or None, request.FILES or None)
        imageForm  =  tbl_crtimages_form(request.POST or None, request.FILES or None)


        # context = {}

        if productDetail.is_valid() and imageForm.is_valid():
            subCatId = request.POST.get('itemSubCategory')
            # print("sub category", subCatId)
            subCat = get_object_or_404(tbl_crt_subcategories, pk=subCatId)

            mstObj = productDetail.save(commit=False)
            
            itemName=productDetail.cleaned_data.get("crt_item_name",None)
            

            # mstObj.crt_item_SKU = "CRT-SKU-" + str(random.randint(100, 999))
            mstObj.crt_item_SKU = createCrtSKU(subCat.crt_sub_category_name,itemName)
            mstObj.crt_item_status = "INACTIVE"
            mstObj.crt_sub_category = subCat
            mstObj.user = request.user

            mstObj.save()


            # for key, value in imageForm.cleaned_data:
            # print(imageForm.cleaned_data)

            first = True
            for key,value in imageForm.cleaned_data.items():
                # print(image,val)
                if value:
                    # print(value,first,mstObj)
                    tbl_crtimages.objects.create(crt_img_url=value, is_primary=first, crt_item_details=mstObj)
                    first = False
            messages.success(request, "Product Added successfully.")
            return redirect("Authentication:creative_items")

        else:
            messages.error(request, "Please correct below errors.")
            context['form'] = productDetail
            context['crtCategory'] = crtCategory
            context['imageForm']=imageForm


    return render(request, template, context)

def edit_creative_product(request, id=None):
    if id :
        template = "account/dashboard/add-product/edit-product.html"
        
        crtCategory = tbl_crt_categories.objects.all()
    
        data = get_object_or_404(tbl_creativeitems_mst, pk=id)
        crt_sub_id = data.crt_sub_category.crt_sub_category_id
        crt_id = data.crt_sub_category.crt_category.crt_category_id
        crtSubCategory = tbl_crt_subcategories.objects.filter(crt_category=crt_id)


        productDetail = tbl_creativeitems_mst_form(instance = data)
        # print(data, crt_id, crt_id)
        productImages = tbl_crtimages.objects.filter(crt_item_details = data)
        context = {
            'crtCategory': crtCategory,
            'crtSubCategory': crtSubCategory,
            'form': productDetail,
            'id': id,
            'crt_id': crt_id,
            'crt_sub_id': crt_sub_id,
            'images': productImages
        }

        if request.method == "POST":
            productDetail = tbl_creativeitems_mst_form(request.POST or None, instance=data)

            if productDetail.is_valid():
                subCatId = request.POST.get('itemSubCategory')
                subCat = get_object_or_404(tbl_crt_subcategories, pk=subCatId)

                itemName=productDetail.cleaned_data.get("crt_item_name",None)

                mstObj = productDetail.save(commit=False)
                SKU=data.crt_item_SKU.split("-")
                # print(SKU)
                newSKU=createCrtSKU(subCat.crt_sub_category_name,itemName)
                newSKU=newSKU.split("-")
                SKU[1]=newSKU[1]
                SKU[2]=newSKU[2]
                SKU='-'.join(i for i in SKU )
                mstObj.crt_item_SKU = SKU
                mstObj.crt_sub_category = subCat
                mstObj.user = request.user
                if mstObj.crt_item_qty >= 1 :
                    mstObj.crt_item_status = "ACTIVE"
                mstObj.save()

                messages.success(request,"Product updated successfully.")
                # print(request.POST)
                return redirect("Authentication:creative_items")
            else:
                messages.error(request, "Please correct above errors.")
                context = {
                    "form": productDetail,
                    'crtCategory': crtCategory,
                    'id': id,
                }

        return render(request, template, context)
    else:
        return redirect("Authentication:creative_items")

def removeCrtItem(request,id=None):
    if id:
        crtItem = tbl_creativeitems_mst.objects.get(crt_item_id=id,user=request.user)
        if tbl_orders_details.objects.filter(crt_item_mst=crtItem).exists():
            messages.warning(request,"Item present in orders, unable to delete.")
        else:
            crtItem.delete()
            messages.success(request,"Your item delete successfully.")
    else:
        messages.error(request, "Some error occured.")
    
    return redirect("Authentication:creative_items")
    

def edit_crt_images(request,id=None,action=None):
    if action== "addItemImage":
        # print(request.POST)
        crt_id = request.POST.get("crt_item_details",None)
        crtItem = tbl_creativeitems_mst.objects.get(crt_item_id=crt_id,user=request.user)
        
        crtImg= tbl_crtimages.objects.filter(crt_item_details=crt_id).count()
        
        if crtImg >= 6:
            messages.error(request,"Sorry, you can upload upto six images only.")
        
        else:
            editImageForm = EditCrtImage(request.POST or None, request.FILES or None)
            if editImageForm.is_valid():
                newImage = editImageForm.save(commit=False)
                newImage.crt_item_details = crtItem
                newImage.save()
                messages.success(request,"Image added successfully.")

            # print("valid")
                    
            else:
                
                messages.error(request,editImageForm.errors['crt_img_url'].as_text())
        
        next = request.POST.get('next', '/')
        return redirect(next)


    if id and request.method=="POST" :
        try:
            images = tbl_crtimages.objects.get(crt_img_id=id)
            
            editImageForm = EditCrtImage(request.POST or None, request.FILES or None)
            next = request.POST.get('next', '/')
            # print(request.FILES)
            if editImageForm.is_valid():
                newImage = editImageForm.save(commit=False)
                images.crt_img_url = newImage.crt_img_url
                images.save()
                messages.success(request,"Image updated successfully.")

                # print("valid")
                
            else:
                # print(editImageForm.errors.as_json())
                messages.error(request,editImageForm.errors['crt_img_url'].as_text())
            
            return redirect(next)

        except tbl_crtimages.DoesNotExist:
            return redirect(next)
    else:
        return redirect("Authentication:creative_items")

def remove_crt_images(request,id=None):
    if id :
        try:
            if tbl_crtimages.objects.filter(crt_img_id=id,is_primary=True).exists():
                
                newPrimary = tbl_crtimages.objects.filter(is_primary=False).first() 
                if newPrimary is not None:
                    newPrimary.is_primary=True
                    newPrimary.save()  
                else:
                    messages.error(request,"There must be atleast one image for item.")
                    next=request.GET.get('next', '/')
                    return redirect(next)

            images = tbl_crtimages.objects.get(crt_img_id=id)
            images.delete()
            next=request.GET.get('next', '/')
            messages.success(request,"Image removed successfully.")
            return redirect(next)

        except tbl_crtimages.DoesNotExist:
            return redirect(next)
    else:
        return redirect("Authentication:creative_items")    

def crtSetPrimary(request,id=None,imgid=None):
    if request.is_ajax():
        if imgid:
            # print("rec")
            imagePrimary = tbl_crtimages.objects.get(is_primary=True,crt_item_details=id)
            imagePrimary.is_primary=False
            imagePrimary.save()
            newimagePrimary = tbl_crtimages.objects.get(crt_img_id=imgid)
            newimagePrimary.is_primary = True
            newimagePrimary.save()
            return JsonResponse({"changed":True})
        else:
            return JsonResponse({"changed":False})

    else:
        raise PermissionDenied


def upload_image(request, id=None):
    form = tbl_crtimages_form(request.POST, request.FILES)

    if form.is_valid():
        photo = form.save(commit=False)
        sub_crt_object = get_object_or_404(tbl_creativeitems_details, crt_item_details_id=id)
        photo.crt_item_details = sub_crt_object
        photo.save()

    else:
        messages.warning(request, "Please correct above errors.")
        context = {'form': form}


def get_sub_category(request, id):
    crtSubCategory = tbl_crt_subcategories.objects.filter(crt_category=id).values()

    return JsonResponse({"subCrtCat": list(crtSubCategory)})


@login_required
def dashboard(request):
    if not request.user.is_superuser:
        template = "account/dashboard/dashboard.html"
        detail = tbl_orders_details.objects.filter(crt_item_mst__user=request.user).values('order').distinct()

        idLst = [d['order'] for d in detail]
        # print(idLst)
        netRevenue = tbl_orders_details.objects.filter(crt_item_mst__user=request.user,item_status=2).aggregate(total=Sum(F('crt_item_qty') * F('unit_price') *0.8 ,output_field=models.DecimalField()))
        print(netRevenue)
        currentOrders = tbl_orders_mst.objects.filter(order_id__in=idLst, delivery_status = 1 ).count()
        completedOrders = tbl_orders_mst.objects.filter(order_id__in=idLst, delivery_status = 3 ).count()
        totalCreativeItems = tbl_creativeitems_mst.objects.filter(user = request.user).count()

        context = {
            "netRevenue": netRevenue,
            "currentOrders": currentOrders,
            "completedOrders": completedOrders,
            "totalCreativeItems": totalCreativeItems,
        }

        return render(request, template, context)
    else:
        return redirect("Authentication:login")



@login_required
def dashboard_profile(request,action=None):
    template = "account/dashboard/dashboard-profile.html"
    UserFormData=EditUserFormData()
    profileFormData=EditProfileForm()
    
    badges= BadgeEntries.objects.filter(user=request.user)
    
    
    try:
        UserAddressData = Address.objects.filter(user_id=request.user.user_id)
        UserDocumentData = Documents.objects.get(user_id=request.user.user_id)
 
    except Address.DoesNotExist:
        UserAddressData = None
    except  Documents.DoesNotExist:
        UserDocumentData = None

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
                    messages.error(request,"Some error occured during image upload. Refreash page and try again please.")
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

            
            messages.success(request,"Updated Successfully.")
            UserFormData=EditUserFormData()
            profileFormData=EditProfileForm()
            return redirect('Authentication:dashboard_profile')                  
            
        else:
            messages.warning(request,"Please correct above errors.")
            
    context={
        "Userform":UserFormData,
        "Profileform":profileFormData,
        "UserAddress":UserAddressData,
        "UserDocument":UserDocumentData,
        "badges":badges
    }
    
    return render(request, template,context)

@login_required
def order_creative(request):
    p = Profile.objects.get(user=request.user)
    if not p.is_verified:
        return HttpResponse("Page not Found.")
    template = "account/dashboard/creative-orders.html"
    oneCancelledItem=False
    
    detail = tbl_orders_details.objects.filter(crt_item_mst__user = request.user).values('order').distinct()
    
    detail = tbl_orders_details.objects.filter(crt_item_mst__user = request.user)
    # idLst = [ d['order'] for d in detail ]
    # orderMst = tbl_orders_mst.objects.filter(order_id__in=idLst)
    
    
    ######### IF item is only one and cancelled then show cancelled as status.
    # ItemCnt=detail.filter()
    

    ##########################
    # print(oneCancelledItem)
    
    # print(idLst)

    # print("BEFORE :: ",orderMst.values("delivery_status"))
    
    # for d in detail:
    #     itm = detail.filter(order_id=d['order']).annotate(cnt=Count("crt_item_mst"))
    #     stCnt=itm.values("item_status").count()
    #     print(d)
    #     if stCnt == 1:
    #         for o in orderMst: 
    #             if o == [*itm.values("order")]:
    #                 print(True)
    #                 print(o,itm.values("order"))
    #                 orderMst=orderMst.upadate(delivery_status=itm.values("item_status"))
            
    # # print("AFTER :: ",orderMst.values("delivery_status"))
    return render(request, template, {'details': detail,"oneCancelledItem":oneCancelledItem})


@login_required
def order_history(request, action='current'):

    if action == 'current':
        title = "Current Orders"
        details = tbl_orders_details.objects.filter(order__user=request.user, item_status=1)
    elif action == 'complete':
        title = "Completed Orders"
        details = tbl_orders_details.objects.filter(order__user=request.user, item_status=2)
    elif action == 'cancel':
        title = "Cancelled Orders"
        details = tbl_orders_details.objects.filter(order__user=request.user, item_status=3)
    elif action == 'return':
        title = "Returned Orders"
        details = tbl_orders_details.objects.filter(order__user=request.user, item_status=5)

    print(details)
    context = {
        'title': title,
        'details': details,
    }
    template = "account/dashboard/order-history.html"
    return render(request, template, context)

@login_required
def order_details(request, id=None):
    template = "account/dashboard/order-details.html"
    
    
    order = tbl_orders_mst.objects.get(order_id=id)
    
    if request.method=='POST':
        
        rate=request.POST.get('item_rating',0.0)
        review=request.POST.get('item_review','')
        redirect_url = request.POST.get("redirect_url","accounts/dashboard/orders/history/")
        crt_item=get_object_or_404(tbl_creativeitems_mst,crt_item_id=request.POST.get('crt_item_id',None))
        if not (Reviews.objects.filter(crt_item=crt_item,user=request.user).exists()):
            reviewForm=Reviews(item_rating=rate,item_review=review,crt_item=crt_item,user=request.user)
            reviewForm.save()
            user=crt_item.user.profile
            rating=user.user_rating
            avg=(float(rating)+float(rate))/2
            user.user_rating=avg
            user.save()
            messages.success(request,"Review Submitted Succesfully")
            return redirect(redirect_url)
        else:
            
            messages.warning(request,"You already reviewed this item.")

    if order.user == request.user:

        orderDetails = tbl_orders_details.objects.filter(order=order)
    else:
        orderDetails = tbl_orders_details.objects.filter(order=order, crt_item_mst__user=request.user)

    totUserItemPrice = 0
    for d in orderDetails:
        totUserItemPrice += d.total_price()
    try:
        payment = Payment.objects.get(order=order)
        # print(payment)
    except Exception as e:
        # print("EXCEPTION::",e)
        payment = None
    # print(orderDetails)
    context = {
        "order": order,
        "details": orderDetails,
        "payment": payment,
        "totUserItemPrice": totUserItemPrice,
    }
    return render(request, template, context)


@login_required
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
                if bool(re.match('[A-Za-z0-9@#$%^&+=]{9,}',pass1)):
                    try:
                        #print(pass1)
                        validate_password(pass1) # for length and strength check
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
                    messages.error(request,"Password does not match given criteria.")
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
                if bool(re.match('[A-Za-z0-9@#$%^&+=]{9,}',password)):
                    try:
                        # print(password)
                        validate_password(password) # for length and strength check
                    except Exception as e:
                        messages.error(request,*e)
                    else:

                        usr = User.objects.get(email=email)
                        usr.set_password(password)
                        usr.save()
                        request.session.delete()
                        return redirect('Authentication:newPasswordDone')
                else:
                    messages.error(request,"Password does not match given criteria.")
                    return redirect('Authentication:newPassword')
            else:
                return render(request,"account/account_active_email_done.html",{"activated":False})
        else:
            messages.error(request,"Passwords do not match.")
            return redirect('Authentication:newPassword')

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
            # print(request.user.user_id)
            documentData=UserDocument(request.POST or None,request.FILES or None)
            #print("Docu Valid",request.user)
            if documentData.is_valid():
                # print("Docu Valid",request.user)
                document = documentData.save(commit=False)
                # usr= User.objects.get(username=request.user)
                document.user = request.user

                #print("Docu Valid",request.user.user_id)

                documentData.pan_img_url = request.FILES['pan_img_url']

                document.save()
            else:
                #print(documentData.errors.as_json)
                messages.error(request,"Please correct below errors.")
            
        context={
            "form":documentData,
        }
        return render(request,template,context)
    else:
        return redirect('Authentication:login')

@login_required
def editDocument(request):
    if request.session.get('user'):
        template = 'account/dashboard/dashboard-profile.html'
        editedData=EditUserDocument()
        UserDocumentData = Documents.objects.get(user_id=request.user.user_id)
        print(UserDocumentData.acc_name)
        if request.method=='POST':
            # print(request.POST)
            editedData=EditUserDocument(request.POST)
            if editedData.is_valid():
                #print("edit valid")
                editedDocu = editedData.save(commit=False)

                UserDocumentData.acc_no=editedDocu.acc_no
                UserDocumentData.acc_name= editedDocu.acc_name
                UserDocumentData.bank_name=editedDocu.bank_name
                UserDocumentData.IFSC_code=editedDocu.IFSC_code
                UserDocumentData.save()

                messages.success(request,"Updated Successfully.")
                editedData=EditUserDocument()
                redirect("Authentication:dashboard_profile")

            else:
                # print(editedData.errors)
                messages.warning(request,"Please correct above errors.")

        context={
            "form":editedData,
            "UserDocument":UserDocumentData,
        }
        return render(request,template,context)
    else:
        return redirect('Authentication:login')




def addAddress(request):

    template = 'account/dashboard/add-address.html'
    state = States.objects.all().order_by("state_name")
    city=None
    if request.session.get('user'):
        addressFormData=AddressForm()
        if request.method=='POST':
            # print(request.POST)
            # response = requests.get('https://api.postalpincode.in/pincode/382213')
            # geodata = response.json()
            # print(geodata)
            city_id = request.POST.get("city")
            state_id = request.POST.get("state")
            print(city_id,state_id)
            addressFormData=AddressForm(request.POST or None)
            if addressFormData.is_valid():
                #print("valid")
                address = addressFormData.save(commit=False)

                if not Address.objects.filter(user_id=request.user.user_id,is_default=True).exists():
                    address.is_default=True
                    
                address.user = request.user
                address.city = Cities.objects.get(city_id=city_id)
                address.state = States.objects.get(state_id=state_id)
                #print(ref_city.city_id)

                address.save()
                messages.success(request,"Your address saved Successfully.")
                addressFormData=AddressForm()
                return redirect("Authentication:dashboard_profile")

            else:
                if city_id:
                    city = Cities.objects.get(city_id=city_id)
                # err=profileForm.errors['user_image']            
                #print(city)
                messages.warning(request,"Please correct below errors.")

        context={
            "form":addressFormData,
            "states":state,
            "selectedCity":city,
        }

        return render(request,template,context)

    else:
        return redirect('Authentication:login')

@login_required()
def editAddress(request,id):
    template = 'account/dashboard/edit-address.html'
    addressFormData=""
    city=""
    state = States.objects.all().order_by("state_name")
    if id:
        addressExist = Address.objects.filter(address_id=id).exists()
        
        if addressExist:
            AddressData = Address.objects.get(address_id=id)
            addressFormData=AddressForm(instance=AddressData)
            city = Cities.objects.get(city_id=AddressData.city_id)
        
            if request.method == "POST" :
                # print(request.POST)
                    city_id = request.POST.get("city")
                    state_id = request.POST.get("state")
                    # print(city_id,state_id)
                    addressFormData=AddressForm(request.POST or None,instance=AddressData)
                    if addressFormData.is_valid():
                        
                        print("valid")
                        address = addressFormData.save(commit=False)
                        address.user = request.user
                        address.city = Cities.objects.get(city_id=city_id)
                        address.state = States.objects.get(state_id=state_id)
                        #print(ref_city.city_id)

                        address.save()
                        messages.success(request,"Your address updated Successfully.")
                        # addressFormData=AddressForm()
                        return redirect("Authentication:dashboard_profile")

                    else:
                        if city_id:
                            city = Cities.objects.get(city_id=city_id)
                                
                        messages.warning(request,"Please correct below errors.")        
            context={
                "form":addressFormData,
                "states":state,
                "selectedCity":city,
            }
            
            return render(request,template,context)

    return redirect("Authentication:dashboard_profile")


@login_required
def delAddress(request,id):
    try:
        if id:
            addressExist = Address.objects.filter(address_id=id).exists()
            

            if addressExist:
                if Address.objects.filter(address_id=id,is_default=True).exists():
                    
                    newDefault = Address.objects.filter(is_default=False).first() # change default address if del addrs is default one
                    newDefault.is_default=True
                    newDefault.save()

                AddressData = Address.objects.get(address_id=id)
                AddressData.delete()

                messages.success(request,"Your address deleted Successfully.")
    except:
        messages.error(request,"Some error occured, Please try after sometime.")

    return redirect("Authentication:dashboard_profile")



def getCities(request,id):
    if request.is_ajax():
        if id:
            #print("rec")
            cities=Cities.objects.filter(state_id=id).values().order_by("city_name")
            return JsonResponse({"cities":list(cities)})
    else:
        raise PermissionDenied

def setDefault(request,id):
    if request.is_ajax():
        if id:
            # print("rec")
            address = Address.objects.get(is_default=True,user=request.user)
            address.is_default=False
            address.save()
            newDefAddress = Address.objects.get(address_id=id)
            newDefAddress.is_default = True
            newDefAddress.save()
            return JsonResponse({"changed":True})
        else:
            return JsonResponse({"changed":False})

    else:
        raise PermissionDenied




def add_scrap_product(request):
    template = "account/dashboard/scp-add-product.html"
    scpCategory = MainScrapCategory.objects.all()

    context = {'scpCategory': scpCategory}

    if request.method == 'POST':
        scpData = tbl_scrapitems_form(request.POST, request.FILES or None)
        imageForm  =  tbl_scpimages_form(request.POST or None, request.FILES or None)

        context={}
        if scpData.is_valid() and imageForm.is_valid():

            subCatId = request.POST.get('itemSubCategory')
            subCat = get_object_or_404(SubScrapCategory, pk=subCatId)
            itemName=scpData.cleaned_data.get("scp_item_name",None)
           
            scpObj = scpData.save(commit=False)
            scpObj.scp_item_SKU = createScpSKU(subCat.scp_sub_category_name,itemName)
            scpObj.scp_item_status = "INACTIVE"
            scpObj.scp_sub_category = subCat
            scpObj.user = request.user
            scpObj.save()
            # print("VALID SAVE IT.")


            first = True
            for key,value in imageForm.cleaned_data.items():
                if value:
                    # print("valid")
                    tbl_scrapimages.objects.create(scp_img_url=value, is_primary=first, scp_item=scpObj)
                    first = False

            messages.success(request, "Product added successfully.")
            return redirect('Authentication:scrap_items')
            
        else:
            messages.error(request, "Please correct above errors.")
            context['form'] = scpData
            context['scpCategory'] = scpCategory
            context['imageForm']=imageForm


    return render(request, template, context)


def get_scp_sub_category(request, id):  #AJAX CATEGORIES
    subScpCat = {}
    scpSubCategory = SubScrapCategory.objects.filter(scp_category=id).values()
    print(scpSubCategory)
    return JsonResponse({"subScpCat": list(scpSubCategory)})



def edit_scrap_product(request, id=None):
    if id:

        template = "account/dashboard/scp-edit-product.html"
        scpCategory = MainScrapCategory.objects.all()
        
        data = get_object_or_404(tbl_scrapitems, pk=id)
        scp_sub_id = data.scp_sub_category.scp_sub_category_id
        scp_id = data.scp_sub_category.scp_category.scp_category_id
        scpSubCategory = SubScrapCategory.objects.filter(scp_category=scp_id)

        productDetail = tbl_scrapitems_form(instance = data)

        productImages = tbl_scrapimages.objects.filter(scp_item = data)

        context = {
            'scpCategory': scpCategory,
            'scpSubCategory': scpSubCategory,
            'form': productDetail,
            'id': id,
            'scp_id': scp_id,
            'scp_sub_id': scp_sub_id,
            'images': productImages
        }

        if request.method == 'POST':
            scpData = tbl_scrapitems_form(request.POST or None, instance=data)

            if scpData.is_valid():
                subCatId = request.POST.get('itemSubCategory')
                subCat = get_object_or_404(SubScrapCategory, pk=subCatId)

                itemName=scpData.cleaned_data.get("scp_item_name",None)

                scpObj = scpData.save(commit=False)
                SKU=data.scp_item_SKU.split("-")
                # print(SKU)
                newSKU=createScpSKU(subCat.scp_sub_category_name,itemName)
                newSKU=newSKU.split("-")
                SKU[1]=newSKU[1]
                SKU[2]=newSKU[2]
                SKU='-'.join(i for i in SKU )
                scpObj.scp_item_SKU = SKU
                scpObj.scp_sub_category = subCat
                scpObj.user = request.user
                # if scpObj.scp_item_qty >= 1 :
                #     scpObj.scp_item_status = "ACTIVE"
                scpObj.save()
                messages.success(request, "Product updated successfully.")
                return redirect('Authentication:scrap_items')
            else:
                messages.error(request, "Please correct above errors.")
                context = {
                    "form": scpData,
                    'scpCategory': scpCategory,
                    'id': id,
                }
        return render(request, template, context)
    else:
        return redirect("Authentication:scrap_items")


def edit_scp_images(request,id=None,action=None):
    if action== "addItemImage":
        # print(request.POST)
        scp_id = request.POST.get("scp_item",None)
        scpItem = tbl_scrapitems.objects.get(scp_item_id=scp_id,user=request.user)
        
        scpImg= tbl_scrapimages.objects.filter(scp_item=scp_id).count()
        
        if scpImg >= 6:
            messages.error(request,"Sorry, you can upload upto six images only.")
        
        else:
            editImageForm = EditScpImage(request.POST or None, request.FILES or None)
            if editImageForm.is_valid():
                newImage = editImageForm.save(commit=False)
                newImage.scp_item = scpItem
                newImage.save()
                messages.success(request,"Image added successfully.")

            # print("valid")
                    
            else:
                messages.error(request,editImageForm.errors['scp_img_url'].as_text())
        
        next = request.POST.get('next', '/')
        return redirect(next)



    if id and request.method=="POST" :
        try:
            images = tbl_scrapimages.objects.get(scp_img_id=id)
            # print(images)
            editImageForm = EditScpImage(request.POST or None, request.FILES or None)
            next = request.POST.get('next', '/')
            # print(request.FILES)
            if editImageForm.is_valid():
                newImage = editImageForm.save(commit=False)
                images.scp_img_url = newImage.scp_img_url
                images.save()  
                messages.success(request,"Image updated successfully.")

                # print("valid")
                
            else:
                # print(editImageForm.errors.as_json())
                messages.error(request,editImageForm.errors['scp_img_url'].as_text())
            
            return redirect(next)

        except tbl_scrapimages.DoesNotExist:
            # print("except")
            return redirect(next)
    else:
        return redirect("Authentication:scrap_items")

def removeScpItem(request,id=None):
    if id:
        scpItem = tbl_scrapitems.objects.get(scp_item_id=id,user=request.user)
        scpItem.delete()
        messages.success(request,"Your item delete successfully.")

    else:
        messages.error(request, "Some error occured.")
    return redirect("Authentication:scrap_items")

def remove_scp_images(request,id=None):
    if id :
        try:
            if tbl_scrapimages.objects.filter(scp_img_id=id,is_primary=True).exists():
                
                newPrimary = tbl_scrapimages.objects.filter(is_primary=False).first()
               
                if newPrimary is not None:
                    newPrimary.is_primary=True
                    newPrimary.save()  
                else:
                    messages.error(request,"There must be atleast one image for item.")
                    next=request.GET.get('next', '/')
                    return redirect(next)
                
            images = tbl_scrapimages.objects.get(scp_img_id=id)
            images.delete()
            
            messages.success(request,"Image removed successfully.")
            next=request.GET.get('next', '/')
            
            return redirect(next)
        except tbl_scrapimages.DoesNotExist:
            return redirect(next)
    else:
        return redirect("Authentication:scrap_items")    

def scpSetPrimary(request,id=None,imgid=None):
    if request.is_ajax():
        if imgid:
            # print("rec")
            imagePrimary = tbl_scrapimages.objects.get(is_primary=True,scp_item=id)
            imagePrimary.is_primary=False
            imagePrimary.save()
            newimagePrimary = tbl_scrapimages.objects.get(scp_img_id=imgid)
            newimagePrimary.is_primary = True
            newimagePrimary.save()
            return JsonResponse({"changed":True})
        else:
            return JsonResponse({"changed":False})

    else:
        raise PermissionDenied

def validate_file_ext(value):
    if not value.name.endswith(('.jpg','.jpeg','.png')):
       return True

def createCrtSKU(subCat,itemName):
    str=''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(4))
    SKU="CRT-"+subCat[0:3].upper()+"-"+itemName[0:3].upper()+"-"+str
    return SKU

def createScpSKU(subCat,itemName):
    str=''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(4))
    SKU="SCP-"+subCat[0:3].upper()+"-"+itemName[0:3].upper()+"-"+str
    return SKU