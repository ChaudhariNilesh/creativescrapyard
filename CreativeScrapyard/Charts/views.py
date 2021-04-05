
from django.db.models.aggregates import Count
from django.shortcuts import render,redirect
from Authentication.models import User,Profile
from Order.models import tbl_orders_details,tbl_orders_mst
from Items.models import *
from CustomAdmin.models import *
from django.core.serializers import serialize
from django.core.exceptions import PermissionDenied
from django.http import Http404, response,HttpResponse,JsonResponse,HttpResponseForbidden

from datetime import datetime 
from django.db.models import Sum, fields,F,DecimalField,ExpressionWrapper
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.db.models.functions import Trunc
@login_required
def charts(request,type=1):

    # template="Charts/chart-admin.html"
    if request.user.is_superuser:
        
        template="Charts/chart-admin.html"
        
        
    else:
        template="Charts/chart-user.html"

        

    context={   
        "chartType":type,

        
    }

    return render(request,template,context)

################################   CAT ITEM WISE   ######################################
@login_required
def catItemCharts(request):
    if request.is_ajax():
        crtCatlabels = []
        crtCatdata = []
        scpCatlabels = []
        scpCatdata = []
        if request.user.is_superuser:
            crtCats = tbl_crt_subcategories.objects.order_by('crt_category__crt_category_name').values("crt_category__crt_category_name").annotate(CrtCnt=Count('tbl_creativeitems_mst'))
        
            scpCats = SubScrapCategory.objects.order_by('scp_category__scp_category_name').values("scp_category__scp_category_name").annotate(ScpCnt=Count('tbl_scrapitems'))
            for cat in crtCats:
                crtCatlabels.append(cat["crt_category__crt_category_name"])
                crtCatdata.append(cat["CrtCnt"])

            for cat in scpCats:
                scpCatlabels.append(cat["scp_category__scp_category_name"])
                scpCatdata.append(cat["ScpCnt"])   
        else:
            crtCats = tbl_creativeitems_mst.objects.filter(user=request.user).order_by('crt_sub_category__crt_category__crt_category_name').values("crt_sub_category__crt_category__crt_category_name").annotate(CrtCnt=Count('crt_item_id'))
            scpCats = tbl_scrapitems.objects.filter(user=request.user).order_by('scp_sub_category__scp_category__scp_category_name').values("scp_sub_category__scp_category__scp_category_name").annotate(ScpCnt=Count('scp_item_id'))
        
            for cat in crtCats:
                crtCatlabels.append(cat["crt_sub_category__crt_category__crt_category_name"])
                crtCatdata.append(cat["CrtCnt"])

            for cat in scpCats:
                scpCatlabels.append(cat["scp_sub_category__scp_category__scp_category_name"])
                scpCatdata.append(cat["ScpCnt"])        

        context={
            "crtCatlabels":crtCatlabels,
            "crtCatdata":crtCatdata,
            "scpCatlabels":scpCatlabels,
            "scpCatdata":scpCatdata,
        }
        return JsonResponse(context)
    else:
        raise PermissionDenied

################################   CAT ORD WISE   ######################################
@login_required
def catOrdCharts(request):
    if request.is_ajax():

        catOrdlabels = []
        catOrddata = []
        if request.user.is_superuser:
            ords = tbl_orders_details.objects.filter(order__order_status=True).order_by('crt_item_mst__crt_sub_category__crt_category__crt_category_name').values("crt_item_mst__crt_sub_category__crt_category__crt_category_name").annotate(OrdCnt=Count('order_details_id'))
        else:
            ords = tbl_orders_details.objects.filter(crt_item_mst__user=request.user,order__order_status=True).order_by('crt_item_mst__crt_sub_category__crt_category__crt_category_name').values("crt_item_mst__crt_sub_category__crt_category__crt_category_name").annotate(OrdCnt=Count('order_details_id'))

        for ord in ords:
            catOrdlabels.append(ord["crt_item_mst__crt_sub_category__crt_category__crt_category_name"])
            catOrddata.append(ord["OrdCnt"])
    
        # ords = tbl_orders_details.objects.filter(order__order_status=True).order_by('crt_item_mst__crt_sub_category__crt_sub_category_name').values("crt_item_mst__crt_sub_category__crt_sub_category_name").annotate(OrdCnt=Count('order_details_id'))
        
        # for ord in ords:
        #     catOrdlabels.append(ord["crt_item_mst__crt_sub_category__crt_sub_category_name"])
        #     catOrddata.append(ord["OrdCnt"])
    
        context={
            "catOrdlabels":catOrdlabels,
            "catOrddata":catOrddata,
        }

        return JsonResponse(context)
    else:
        raise PermissionDenied
    
################################   ITEMS STATUS   ######################################
@login_required
def itemsCharts(request):
    
    if request.is_ajax():
        itemLabels = []
        itemData = []
        scpItemlabels = []
        scpItemdata = []
    
        if request.user.is_superuser:
            crtCats = tbl_creativeitems_mst.objects.values("crt_item_status").annotate(itemCnt=Count('crt_item_status'))
            scpCats = tbl_scrapitems.objects.values("scp_item_status").annotate(ScpCnt=Count('scp_item_status'))
        
        else:
            crtCats = tbl_creativeitems_mst.objects.filter(user=request.user).values("crt_item_status").annotate(itemCnt=Count('crt_item_status'))
            scpCats = tbl_scrapitems.objects.filter(user=request.user).values("scp_item_status").annotate(ScpCnt=Count('scp_item_status'))

        for crtCat in crtCats:
            itemLabels.append(crtCat["crt_item_status"])
            itemData.append(crtCat["itemCnt"])
        
        for cat in scpCats:
            scpItemlabels.append(cat["scp_item_status"])
            scpItemdata.append(cat["ScpCnt"])        

        context={
            "itemLabels":itemLabels,
            "itemData":itemData,       
            "scpItemlabels":scpItemlabels,
            "scpItemdata":scpItemdata,
        }
        return JsonResponse(context)
    else:
        raise PermissionDenied


################################   USER STATUS   ######################################
@login_required
def userCharts(request):
    if request.user.is_superuser and request.is_ajax():
        usrLabels = []
        usrData = []
        
        usr = User.objects.filter(is_superuser=False).values("is_active").annotate(actCnt=Count('is_active'))
        profile = Profile.objects.filter(user__is_superuser=False).values("is_verified").annotate(verCnt=Count('is_verified'))

        print(usr)
        print(profile)

        for u in usr:
            if u["is_active"]:
                usrLabels.append("ACTIVE")
            else:
                usrLabels.append("INACTIVE")
            
            usrData.append(u["actCnt"])

        for p in profile:
            if p["is_verified"]:
                usrLabels.append("VERIFIED")
            else:
                usrLabels.append("NOT VERIFIED")
                
            usrData.append(p["verCnt"])


        context={
            "usrLabels":usrLabels,
            "usrData":usrData,
        }
        # print(context)
        return JsonResponse(context)
    else:
        raise PermissionDenied

        


def monOrds(request):
    if request.is_ajax():

        monOrdlabels = ["January","February","March","April","May","June","July","August","September","October","November","December"]
        monOrddata = []
        ordMont={}


        if request.user.is_superuser:

            order_month = tbl_orders_mst.objects\
            .annotate(order_month=Trunc('order_date', 'month'))\
            .values('order_month')\
            .annotate(orderCnt=Count('order_id'))
            for o in order_month:
                ordMont[(o['order_month'].strftime("%B"))]=o['orderCnt']
        else:
        
            order_month = tbl_orders_mst.objects.filter(tbl_orders_details__crt_item_mst__user=request.user,order_status=True)\
            .annotate(order_month=Trunc('order_date', 'month'))\
            .values('order_month')\
            .annotate(orderCnt=Count('order_id'))    
            
            for o in order_month:
                ordMont[(o['order_month'].strftime("%B"))]=o['orderCnt']
        
        for m in monOrdlabels:
                if m in ordMont:
                    
                    monOrddata.append(ordMont[m])
                else: 
                    monOrddata.append(0)

            
        context={
            "monOrdlabels":monOrdlabels,
            "monOrddata":monOrddata,
        }
        
        return JsonResponse(context)

    else:
        raise PermissionDenied

def monSales(request):
    monSallabels = ["January","February","March","April","May","June","July","August","September","October","November","December"]
    monSaldata = []
    if request.is_ajax():
        if request.user.is_superuser:
            order_month = tbl_orders_mst.objects.filter(delivery_status=3)\
            .annotate(order_month=Trunc('order_date', 'month'))\
            .values('order_month')\
            .annotate(orderCnt=Count('order_id'))
            ordMont={}
        else:
            order_month = tbl_orders_mst.objects.filter(delivery_status=3,tbl_orders_details__crt_item_mst__user=request.user,order_status=True)\
            .annotate(order_month=Trunc('order_date', 'month'))\
            .values('order_month')\
            .annotate(orderCnt=Count('order_id'))
            ordMont={}            

    
        for o in order_month:
            ordMont[(o['order_month'].strftime("%B"))]=o['orderCnt']
        
        for m in monSallabels:
                if m in ordMont:
                    
                    monSaldata.append(ordMont[m])
                else: 
                    monSaldata.append(0)

            
        context={
            "monSallabels":monSallabels,
            "monSaldata":monSaldata,
        }
        
        return JsonResponse(context)

    else:
        raise PermissionDenied
