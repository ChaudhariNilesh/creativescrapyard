from django.db.models.aggregates import Count
from django.db.models.query_utils import Q
from django.shortcuts import render,redirect
from Authentication.models import User
from Order.models import tbl_orders_details
from Items.models import *
from django.core.serializers import serialize
from django.core.exceptions import PermissionDenied
from django.http import Http404, response,HttpResponse
from datetime import datetime 
from django.db.models import Sum, fields,F,DecimalField,ExpressionWrapper
from django.utils import timezone
from .utils import render_to_pdf
from .filters import *

# from django.template.loader import render_to_string
# from weasyprint import HTML
# import tempfile


# from slick_reporting.views import SlickReportView
# from slick_reporting.fields import SlickReportField


# Create your views here.
def reports(request):
    users = User.objects.filter(is_superuser=False)
    # data = list(users.values())
    data = serialize("json",users,fields=("user_id,username,email,date_created,is_active,is_verified")) 
    # crtItems = tbl_creativeitems_mst.objects.filter(crt_item_status="ACTIVE")
    # data = serialize("json",list(crtItems),fields=("pk","crt_item_name","crt_sub_category"))   
    print(data)
    context={"user":data}
    return render(request, 'UserReports/report.html',context)


def productReports(request,by=None,search=None,export=None):
    if not request.user.is_superuser and request.user.is_active:
        exportList=['pdf']
        
        crtItems = tbl_creativeitems_mst.objects.filter(user=request.user)
        crtItem_filter = ProductFilter(request.POST, queryset=crtItems)
        # print(crtItem_filter.qs)
        context={"items":crtItems,"filter":crtItem_filter}
        
        if request.POST.get("action")=="export":
            crtItem_filter = ProductFilter(request.POST, queryset=crtItems)
            today = timezone.now()
            filter_by=""
            for k,v in request.POST.items():
                if v and k!="csrfmiddlewaretoken" and k!="action":                    
                    filter_by+=str(k)+","
                    filter_by = filter_by.replace('_',' ').title()           
            context = {
                'reportType':'crt-report',
                'today': today,
                'items': crtItem_filter.qs,
                'request': request,
                'qtyCnt':crtItem_filter.qs.aggregate(itemCount=Sum('crt_item_qty')),
                'totalCost':crtItem_filter.qs.aggregate(cost=Sum(ExpressionWrapper(F('crt_item_qty')*F("crt_item_price"),output_field=DecimalField()))),
                'summary':crtItem_filter.qs.values('crt_item_status').annotate(itemStatus=Count('crt_item_status')),
                'filter_by':filter_by
            }
            pdf = render_to_pdf('UserReports/report-pdf.html', context)
            
            if pdf:
                response = HttpResponse(pdf, content_type='application/pdf')
                filename = "Creative-Item-Report_%s.pdf" %(str(datetime.now()))
                content = "inline; filename=%s" %(filename)
                download = request.GET.get("download")
                if download:
                    content = "attachment; filename=%s" %(filename)
                response['Content-Disposition'] = content
                return response

            return HttpResponse("Not found")


        else:
            return render(request, 'UserReports/product-report.html',context)
    else:
        return redirect('Authentication:login')

def scpItemsReports(request,by=None,search=None,export=None):
    if not request.user.is_superuser and request.user.is_active:
        exportList=['pdf']
        
        scpItems = tbl_scrapitems.objects.filter(user=request.user)
        scpItem_filter = ScrapItemFilter(request.POST, queryset=scpItems)
        # print(scpItem_filter.qs)
        context={"items":scpItems,"filter":scpItem_filter}
        
        if request.POST.get("action")=="export":
            scpItem_filter = ScrapItemFilter(request.POST, queryset=scpItems)
            today = timezone.now()
            filter_by=""
            for k,v in request.POST.items():
                if v and k!="csrfmiddlewaretoken" and k!="action":                    
                    filter_by+=str(k)+","
                    filter_by = filter_by.replace('_',' ').title()
            context = {
                'reportType':'scp-report',
                'today': today,
                'items': scpItem_filter.qs,
                'request': request,
                'qtyCnt':scpItem_filter.qs.aggregate(itemCount=Sum('scp_item_qty')),
                'totalCost':scpItem_filter.qs.aggregate(cost=Sum(ExpressionWrapper(F('scp_item_qty')*F("scp_item_price"),output_field=DecimalField()))),
                'summary':scpItem_filter.qs.values('scp_item_status').annotate(itemStatus=Count('scp_item_status')),
                'filter_by':filter_by
            }
            pdf = render_to_pdf('UserReports/report-pdf.html', context)
            
            if pdf:
                response = HttpResponse(pdf, content_type='application/pdf')
                filename = "Scrap-Item-Report_%s.pdf" %(str(datetime.now()))
                content = "inline; filename=%s" %(filename)
                download = request.GET.get("download")
                if download:
                    content = "attachment; filename=%s" %(filename)
                response['Content-Disposition'] = content
                return response

            return HttpResponse("Not found")


        else:
            return render(request, 'UserReports/scrap-report.html',context)
    else:
        return redirect('Authentication:login')


def orderReports(request,export=None):
    if not request.user.is_superuser and request.user.is_active:
        orderDet = tbl_orders_details.objects.filter(order__order_status=True,crt_item_mst__user=request.user)
        
        orderDet_filter = OrderFilter(request.POST, queryset=orderDet)
        # print(orderDet_filter.qs.values())
        # comm=orderDet_filter.qs.aggregate(orderComm = Sum(ExpressionWrapper(F('crt_item_qty') * F('unit_price')*0.2,output_field=DecimalField())))
        # print(comm) 
        context={"orderDet":orderDet,"filter":orderDet_filter}
        
        if request.POST.get("action")=="export":
            orderDet_filter = OrderFilter(request.POST, queryset=orderDet)
            today = timezone.now()
            filter_by=""
            for k,v in request.POST.items():
                if v and k!="csrfmiddlewaretoken" and k!="action":                    
                    filter_by+=str(k)+","
                    filter_by = filter_by.replace('_',' ').title()
        
            context = {
                'reportType':'orderDet-report',
                'today': today,
                'orderDet': orderDet_filter.qs,
                'request': request,
                'status':orderDet_filter.qs.values('item_status').annotate(statusCount=Count('item_status')),
                'cnt':orderDet_filter.qs.aggregate(orderCount=Count('order_details_id')),
                'ordQty':orderDet_filter.qs.aggregate(itemCount=Sum('crt_item_qty')),
                'ordUnit':orderDet_filter.qs.aggregate(TotalunitPrice=Sum('unit_price')),
                'ordTot':orderDet_filter.qs.aggregate(TotalPrice=Sum(ExpressionWrapper(F('crt_item_qty')*F("unit_price"),output_field=DecimalField()))),
                'ordComm':orderDet_filter.qs.aggregate(TotalComm = Sum(ExpressionWrapper(F('crt_item_qty') * F('unit_price')*0.2,output_field=DecimalField()),filter=Q(item_status=2))),
                'ordDelivered':orderDet_filter.qs.aggregate(price=Sum(ExpressionWrapper(F('crt_item_qty')*F("unit_price"),output_field=DecimalField()),filter=Q(item_status=2))),
                'filter_by':filter_by
            }
            
            pdf = render_to_pdf('UserReports/report-pdf.html', context)
            
            if pdf:
                response = HttpResponse(pdf, content_type='application/pdf')
                filename = "Orders-Report_%s.pdf" %(str(datetime.now()))
                content = "inline; filename=%s" %(filename)
                download = request.GET.get("download")
                if download:
                    content = "attachment; filename=%s" %(filename)
                response['Content-Disposition'] = content
                return response

            return HttpResponse("Not found")

        
        else:
            return render(request, 'UserReports/orders-report.html',context)
    else:
        return redirect('Authentication:login')
