from django.db.models.aggregates import Count
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
    return render(request, 'Reports/report.html',context)


def productReports(request,by=None,search=None,export=None):
    if request.user.is_superuser:
        exportList=['pdf']
        
        crtItems = tbl_creativeitems_mst.objects.filter()
        crtItem_filter = ProductFilter(request.POST, queryset=crtItems)
        # print(crtItem_filter.qs)
        filter_by=""
        for k,v in request.POST.items():
            if v and k!="csrfmiddlewaretoken" and k!="action":                    
                filter_by+=str(k)+","
                filter_by = filter_by.replace('_',' ').title()

        context={"items":crtItems,"filter":crtItem_filter}
        
        if request.POST.get("action")=="export":
            crtItem_filter = ProductFilter(request.POST, queryset=crtItems)
            today = timezone.now()
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
            print(context['summary'])
            pdf = render_to_pdf('Reports/report-pdf.html', context)
            
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
            return render(request, 'Reports/product-report.html',context)
    else:
        return redirect('CustomAdmin:login')

def scpItemsReports(request,by=None,search=None,export=None):
    if request.user.is_superuser:
        exportList=['pdf']
        
        scpItems = tbl_scrapitems.objects.filter()
        scpItem_filter = ScrapItemFilter(request.POST, queryset=scpItems)
        # print(scpItem_filter.qs)
        context={"items":scpItems,"filter":scpItem_filter}
        
        if request.POST.get("action")=="export":
            scpItem_filter = ScrapItemFilter(request.POST, queryset=scpItems)
            
            filter_by=""
            for k,v in request.POST.items():
                if v and k!="csrfmiddlewaretoken" and k!="action":                    
                    filter_by+=str(k)+","
                    filter_by = filter_by.replace('_',' ').title()


            today = timezone.now()
            
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
            pdf = render_to_pdf('Reports/report-pdf.html', context)
            
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
            return render(request, 'Reports/scrap-report.html',context)
    else:
        return redirect('CustomAdmin:login')
    

def userReports(request,export=None):
    
    if request.user.is_superuser:
        # crtItems = tbl_creativeitems_mst.objects.filter()
        users = User.objects.filter(is_superuser=False)
        
        user_filter = UserFilter(request.POST, queryset=users)
        # print(user_filter.qs)
        context={"users":users,"filter":user_filter}
        
        if request.POST.get("action")=="export":
            user_filter = UserFilter(request.POST, queryset=users)
            filter_by=""
            
            for k,v in request.POST.items():
                if v and k!="csrfmiddlewaretoken" and k!="action":                    
                    filter_by+=str(k)+","
                    filter_by = filter_by.replace('_',' ').title()
            
            today = timezone.now()
            context = {
                'reportType':'usr-report',
                'today': today,
                'users': user_filter.qs,
                'request': request,
                'cnt':user_filter.qs.aggregate(activeCount=Sum('is_active'),artistCount=Sum('profile__is_verified')),
                'filter_by':filter_by
            }
            pdf = render_to_pdf('Reports/report-pdf.html', context)
            
            if pdf:
                response = HttpResponse(pdf, content_type='application/pdf')
                filename = "Users-Report_%s.pdf" %(str(datetime.now()))
                content = "inline; filename=%s" %(filename)
                download = request.GET.get("download")
                if download:
                    content = "attachment; filename=%s" %(filename)
                response['Content-Disposition'] = content
                return response

            return HttpResponse("Not found")

        
        else:
            return render(request, 'Reports/user-report.html',context)
    else:
        return redirect('CustomAdmin:login')

def orderReports(request,export=None):
    if request.user.is_superuser:
        orderDet = tbl_orders_details.objects.filter(order__order_status=True)
        
        orderDet_filter = OrderFilter(request.POST, queryset=orderDet)
        # print(orderDet_filter.qs.values())
        context={"orderDet":orderDet,"filter":orderDet_filter}
        
        if request.POST.get("action")=="export":

            filter_by=""
            for k,v in request.POST.items():
                if v and k!="csrfmiddlewaretoken" and k!="action":                    
                    filter_by+=str(k)+","
                    filter_by = filter_by.replace('_',' ').title()


            orderDet_filter = OrderFilter(request.POST, queryset=orderDet)
            today = timezone.now()
            # print(orderDet_filter.form)
            
        
            context = {
                'reportType':'orderDet-report',
                'today': today,
                'orderDet': orderDet_filter.qs,
                'request': request,
                'status':orderDet_filter.qs.values('item_status').annotate(statusCount=Count('item_status')),
                'cnt':orderDet_filter.qs.aggregate(orderCount=Count('order_details_id')),
                'filter_by':filter_by
            }
            pdf = render_to_pdf('Reports/report-pdf.html', context)
            
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
            return render(request, 'Reports/orders-report.html',context)
    else:
        return redirect('CustomAdmin:login')

    



    
    






















    # if export in exportList:
         
        
    #     if by is not None and search is not None:
    #         if by=="0":  #ITEM ID
    #             # print(by,search)
    #             crtItems=tbl_creativeitems_mst.objects.filter(crt_item_status="ACTIVE",crt_item_id=int(search))
    #             # print(crtItems)

    #     today = timezone.now()
    #     context = {
    #         'today': today,
    #         'items': crtItem_filter.qs,
    #         'request': request,
    #         'qtyCnt':tbl_creativeitems_mst.objects.filter(crt_item_status="ACTIVE").aggregate(itemCount=Sum('crt_item_qty'))
    #     }
    #     # print(context)
        
    #     # data = {'today': datetime.date.today(),'amount': 39.99,'customer_name': 'Cooper Mann','order_id': 1233434,}
    #     pdf = render_to_pdf('Reports/report-pdf.html', context)
        
    #     if pdf:
    #         response = HttpResponse(pdf, content_type='application/pdf')
    #         filename = "Creative-Item-Report_%s.pdf" %(str(datetime.datetime.now()))
    #         content = "inline; filename=%s" %(filename)
    #         download = request.GET.get("download")
    #         if download:
    #             content = "attachment; filename=%s" %(filename)
    #         response['Content-Disposition'] = content
    #         return response
    #     return HttpResponse("Not found")
        

# class MonthlyProductSales(SlickReportView):
#     # The model where you have the data
#     report_model = tbl_orders_details
    
#     # the main date field used for the model.
#     date_field = 'order__order_date' # or 'order__date_placed'
#     # this support traversing, like so
#     # date_field = 'order__date_placed'

#     # A foreign key to group calculation on
#     # group_by = 'is_verified'

#     # The columns you want to display
#     columns = ['pickup_address']

#     # Charts
#     charts_settings = [
#      {
#         'type': 'bar',
#         'data_source': 'value__sum',
#         'title_source': 'title',
#      },
#     ]
    
