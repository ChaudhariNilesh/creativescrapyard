from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from .forms import *
from CustomAdmin.models import *
from Items.forms import *
from Items.models import *
from django.contrib import messages
from django.http import JsonResponse
import random
# Create your views here.

def login(request):
    template = "Home/login.html"
    return render(request, template)


def signup(request):
    template = "Home/registration.html"
    if request.method == "POST":
        pass
        # print(request.POST)
    return render(request, template)


def passwordReset(request):
    template = "account/password_reset.html"
    return render(request, template)


def passwordResetLink(request):
    template = "account/password_reset_done.html"
    return render(request, template)


def newPassword(request):
    template = "account/password_reset_from_key.html"
    return render(request, template)


def newPasswordDone(request):
    template = "account/password_reset_from_key_done.html"
    return render(request, template)


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


def add_creative_product(request, action=None):
    # print("action: ", action)
    itemMainData = tbl_creativeitems_mst_form()
    crtCategory = tbl_crt_categories.objects.all()
    template = "account/dashboard/add-product/add-product-1.html"
    if request.method == 'GET':
        crtCategory = tbl_crt_categories.objects.all()
        context = {'crtCategory': crtCategory}
        # return render(request, template)

    elif request.method == "POST" and action == 'mainDetail':
        itemMainData = tbl_creativeitems_mst_form(request.POST)  # instance=request.user

        if itemMainData.is_valid():
            crt_id = request.POST.get('itemSubCategory')

            obj = itemMainData.save(commit=False)
            crtSubCategoryObject = get_object_or_404(tbl_crt_subcategories, pk=crt_id)
            obj.crt_sub_category = crtSubCategoryObject
            obj.save()

            obj_id = obj.crt_item_id
            request.session['itemMstId'] = obj_id
            url = '/accounts/dashboard/product/creative/add/item/' + str(obj_id)
            return redirect(url)

        else:
            messages.warning(request, "Please correct above errors.")
            context = {"form": itemMainData, 'crtCategory': crtCategory, }

    return render(request, template, context)


def add_creative_product_detail(request, id=None):
    template = "account/dashboard/add-product/add-product-2.html"
    context = {'item_id': id, 'error' : False}
    # item = get_object_or_404(tbl_creativeitems_mst, pk=id)

    # check requesting user is related to the requested item.
    # if item.user != request.user:
    #     generate error

    if request.method == 'POST':
        ItemDetaildata = tbl_creativeitems_details_form(request.POST, request.FILES or None)  # instance=request.user

        imageslist = request.FILES.getlist('crt_img_url')
        totImage=0
        for image in imageslist:
            totImage += 1
            print(image)
            imageValidExt = imageValidLen = True
            print(validate_file_ext(image))
            if validate_file_ext(image):
                imageValidExt = False
                break
            elif totImage > 6:
                imageValidLen = False
                break


        if ItemDetaildata.is_valid() and imageValidExt and imageValidLen :

            obj = ItemDetaildata.save(commit=False)
            crt_mst_id = get_object_or_404(tbl_creativeitems_mst,crt_item_id=id)
            obj.crt_item = crt_mst_id
            obj.crt_item_SKU = 'ABC-EFG' + str(random.randint(3, 9000))
            obj.save()
            sub_cat_id = obj.crt_item_details_id
            first = True
            for image in imageslist:
                tbl_crtimages.objects.create(crt_img_url=image, is_primary=first ,crt_item_details=obj)
                first = False
                # else:
                #     tbl_crtimages.objects.create(crt_img_url=image, is_primary=False, crt_item_details=obj)
            context = {
                'item_id': id,
                'sub_cat_id': sub_cat_id,
            }

        else:
            messages.warning(request, "Please correct above errors.")
            # print(ItemDetaildata.errors.as_json)
            if imageValidExt or imageValidLen:
                context = {
                    "form": ItemDetaildata,
                    'item_id': id,
                    'image_error': "Maximum 6 images are allowed. Only '.jpg, .jpeg, .png'  are allowed",
                    'error':True,
                }
            else:
                context = {
                    "form": ItemDetaildata,
                    'item_id': id,
                }


    return render(request, template, context)


# def add_photo(request, id=None):
#     if request.is_ajax() and request.method == 'POST':
#         form = tbl_crtimages_form(request.POST, request.FILES)
#         # print(request.POST)
#         # print(request.FILES)
#
#         if form.is_valid():
#             photo = form.save(commit=False)
#             sub_crt_object = get_object_or_404(tbl_creativeitems_details, crt_item_details_id=id)
#             photo.crt_item_details = sub_crt_object
#             photo.save()
#             basename=os.path.basename(photo.crt_img_url.path)
#             print(basename)
#             data = {'id': photo.crt_img_id,'image_name':basename,'url': photo.crt_img_url.path, 'is_valid': True}
#         else:
#             print(form.errors.as_json)
#             data = {'is_valid': False}
#         return JsonResponse({"data":data})

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
    subCrtCat = {}
    crtSubCategory = tbl_crt_subcategories.objects.filter(crt_category=id).values()

    return JsonResponse({"subCrtCat": list(crtSubCategory)})





# def product_photo_remove(request, pk):
#     template = 'account/dashboard/add-product/add-product-2.html'
#     img_obj = get_object_or_404(tbl_crtimages, crt_img_id=pk)
#     sub_cat_object = img_obj.crt_item_details.crt_item_details_id
#     item_id = img_obj.crt_item_details.crt_item.crt_item_id
#     context = {
#         'item_id': item_id,
#         'sub_cat_id': sub_cat_object,
#     }
#     tbl_crtimages.objects.get(crt_img_id=pk).delete()
#     return redirect('Authentication:add_creative_product_detail', item_id='item_id')
#     # return render(request, template, context)


def dashboard(request):
    template = "account/dashboard/dashboard.html"
    return render(request, template)


def add_document(request):
    template = "account/dashboard/document.html"
    return render(request, template)


def dashboard_profile(request):
    template = "account/dashboard/dashboard-profile.html"
    return render(request, template)


def order_creative(request):
    template = "account/dashboard/creative-orders.html"
    return render(request, template)


def order_history(request, action='current'):
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



def add_scrap_product(request):
    template = "account/dashboard/scp-add-product.html"
    scpCategory = MainScrapCategory.objects.all()

    if request.method == 'GET':
        context = {'scpCategory': scpCategory}

    elif request.method == 'POST':
        scpData = tbl_scrapitems_form(request.POST, request.FILES or None)

        imageslist = request.FILES.getlist('scp_img_url')
        totImage = 0

        for image in imageslist:
            totImage += 1
            print(image)
            imageValidExt = imageValidLen = True
            print(validate_file_ext(image))
            if validate_file_ext(image):
                imageValidExt = False
                break
            elif totImage > 6:
                imageValidLen = False
                break

        if scpData.is_valid() and imageValidExt and imageValidLen:
            # scpData.save(commit=False)

            obj = scpData.save(commit=False)
            obj.scp_item_SKU = 'SCP-EFG-' + str(random.randint(3, 9000))
            obj.save()

            first = True
            for image in imageslist:
                tbl_scrapimages.objects.create(scp_img_url=image, is_primary=first, scp_item=obj)
                first = False
            return redirect('Authentication:scrap_items')
            # context = {"form": scpData, 'scpCategory': scpCategory, }
        else:
            messages.warning(request, "Please correct above errors.")
            if imageValidExt or imageValidLen:
                context = {
                    "form": scpData,
                    'scpCategory': scpCategory,
                    'image_error': "Maximum 6 images are allowed. Only '.jpg, .jpeg, .png'  are allowed",
                    'error':True,
                }
            else:
                context = {"form": scpData, 'scpCategory': scpCategory, }

    return render(request, template, context)

def get_scp_sub_category(request, id):
    subScpCat = {}
    scpSubCategory = SubScrapCategory.objects.filter(scp_category=id).values()
    print(scpSubCategory)
    return JsonResponse({"subScpCat": list(scpSubCategory)})


def edit_creative_product(request, id=None):
    template = "account/dashboard/add-product/edit-product.html"
    crtCategory = tbl_crt_categories.objects.all()

    if request.method == "GET":
        context = {'crtCategory': crtCategory, 'id': id}

    elif request.method == "POST":
        mst_data = tbl_creativeitems_mst_form(request.POST or None)
        detail_data = tbl_creativeitems_details_form(request.POST or None, request.FILES or None)

        imageslist = request.FILES.getlist('crt_img_url')
        totImage = 0

        for image in imageslist:
            totImage += 1
            print(image)
            imageValidExt = imageValidLen = True
            print(validate_file_ext(image))
            if validate_file_ext(image):
                imageValidExt = False
                break
            elif totImage > 6:
                imageValidLen = False
                break


        if mst_data.is_valid() and detail_data.is_valid() and imageValidExt and imageValidLen:

            # first = True
            # for image in imageslist:
            #     tbl_crtimages.objects.create(crt_img_url=image, is_primary=first, crt_item_details=obj)
            #     first = False

            url = '/accounts/dashboard/product/creative/add/item/' + str(obj_id)
            return redirect(url)
        else:
            messages.warning(request, "Please correct above errors.")

            if imageValidExt or imageValidLen:
                context = {
                    "mst": mst_data,
                    'detail': detail_data,
                    'crtCategory': crtCategory,
                    'id': id,
                    'image_error': "Maximum 6 images are allowed. Only '.jpg, .jpeg, .png'  are allowed",
                    'error':True,
                }
            else:
                context = {"mst": mst_data, 'detail': detail_data, 'crtCategory': crtCategory, 'id': id}

    return render(request, template, context)


def edit_scrap_product(request, id=None):
    template = "account/dashboard/scp-edit-product.html"
    scpCategory = MainScrapCategory.objects.all()

    if request.method == 'GET':
        context = {'scpCategory': scpCategory}

    elif request.method == 'POST':
        scpData = tbl_scrapitems_form(request.POST, request.FILES or None)
        # scpImgData = tbl_scrapimages_form(request.POST, request.FILES or None)

        imageslist = request.FILES.getlist('scp_img_url')
        print(request.FILES)
        totImage=0

        for image in imageslist:
            totImage+=1
            print(image)
            imageValidExt=imageValidLen=True
            print(validate_file_ext(image))
            if  validate_file_ext(image):
                imageValidExt = False
                break
            elif totImage>6:
                imageValidLen = False
                break


        if scpData.is_valid() and imageValidExt and imageValidLen:
            # scpData.save(commit=False)

            # obj = scpData.save(commit=False)
            # obj.scp_item_SKU = 'SCP-EFG-' + str(random.randint(3, 9000))
            # obj.save()
            #
            # first = True
            # for image in imageslist:
            #     tbl_scrapimages.objects.create(scp_img_url=image, is_primary=first, scp_item=obj)
            #     first = False

            return redirect('Authentication:scrap_items')
        else:
            messages.warning(request, "Please correct above errors.")
            if imageValidExt or imageValidLen:

                context = {
                    "form": scpData,
                    'scpCategory': scpCategory,
                    'image_error': "Maximum 6 images are allowed. Only '.jpg, .jpeg, .png'  are allowed",
                    'error':True,
                }
            else:
                context = {"form": scpData, 'scpCategory': scpCategory}

    return render(request, template, context)


def validate_file_ext(value):
    if not value.name.endswith(('.jpg','.jpeg','.png')):
       return True