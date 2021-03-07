from django.http.response import JsonResponse
from CreativeScrapyard import settings
from django.shortcuts import render,redirect,HttpResponse,get_object_or_404
from .forms import *
from .models import *
import random


# Create your views here.

def creativeSingleItem(request,id):
    template = 'Shop/single-item.html'
    artist=None
    artist_products=None
    images=None
    product=get_object_or_404(tbl_creativeitems_mst,crt_item_id=id)
    all_products=tbl_creativeitems_mst.objects.filter(crt_item_status="ACTIVE")
    # print(all_products)
    ids=all_products.values_list('crt_item_id',flat=True)
    # print(ids)
    
    r_ids = random.sample(list(ids), 3)
 
    explore_products=all_products.filter(crt_item_id__in=r_ids)

    
    if product:
        artist=product.user
        artist_products=tbl_creativeitems_mst.objects.filter(user=artist)
    images = tbl_crtimages.objects.filter(crt_item_details_id=id)
    context={
    'is_creative':True,
    'product':product,
    'images':images,
    'artist_products':artist_products,
    'explore_products':explore_products
    }
    return render(request,template,context)

def scrapSingleItem(request,id):
    template = 'Shop/single-item.html'
    seller=None
    seller_products=None
    images=None
    product=get_object_or_404(tbl_scrapitems,scp_item_id=id)
    all_products=tbl_scrapitems.objects.filter(scp_item_status="ACTIVE")
    print(all_products)
    ids=all_products.values_list('scp_item_id',flat=True)
    print(ids)
    
    r_ids = random.sample(list(ids), 1)
 
    explore_products=all_products.filter(scp_item_id__in=r_ids)

    
    if product:
        seller=product.user
        seller_products=tbl_scrapitems.objects.filter(user=seller)
    images = tbl_scrapimages.objects.filter(scp_item_id=id)
    context={
    'is_scrap':True,
    'product':product,
    'images':images,
    'artist_products':seller_products,
    'explore_products':explore_products
    }
    return render(request,template,context)

def reportIssue(request):
    issue_msg=""
    issue_sub=""
    if request.method == "POST":
        # print(request.POST)
        issueForm = ReportIssueForm(request.POST)
        if issueForm.is_valid():
            if request.POST.get("issue_type")=='1':
                    issue = issueForm.save(commit=False)
                    print(issue)
                    issue.crt_item = int(request.POST.get("crt_item_id",None))  #find crt the product.     
                    issue.reported_user_id=None           
                    issue.user = request.user
                    issue.save()
                    
            elif request.POST.get("issue_type")=='2':
                    issue = issueForm.save(commit=False)
                    issue.reported_user_id=None
                    issue.scp_item = int(request.POST.get("scp_item_id",None))
                    issue.user = request.user
                    issue.save()

            elif request.POST.get("issue_type")=='3':
                # print("USER")
                issue = issueForm.save(commit=False)
                user_id=request.POST.get("user_id")
                if User.objects.filter(user_id=user_id).exists():
                    reportee = User.objects.get(user_id=user_id)
                    issue.reported_user_id = reportee.user_id # find the product related user.
                    issue.user = request.user
                    issue.save()

            return JsonResponse({"errors":False})

        else:
        
            if 'issue_sub' in issueForm.errors:
                issue_sub=issueForm.errors["issue_sub"].as_text()
            if 'issue_msg' in issueForm.errors:
                issue_msg=issueForm.errors["issue_msg"].as_text()
            msg={
                "issue_sub":issue_sub,
                "issue_msg":issue_msg,
            }
            return JsonResponse({"errors":msg})
        
        
        # return redirect("Home:Items:creativeSingleItem")
    