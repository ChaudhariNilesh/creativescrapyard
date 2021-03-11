from datetime import datetime
from django.shortcuts import render
from Authentication.models import User
from Order.models import tbl_orders_details
from Items.models import *
from django.core.serializers import serialize
from django.core.exceptions import PermissionDenied
from django.http import Http404, response,HttpResponse
import datetime
from django.db.models import Sum, fields,F,DecimalField,ExpressionWrapper
from django.utils import timezone
from .utils import render_to_pdf
from .filters import ProductFilter

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
    exportList=['pdf']
    
    crtItems = tbl_creativeitems_mst.objects.filter()
    crtItem_filter = ProductFilter(request.POST, queryset=crtItems)
    # print(crtItem_filter.qs)
    context={"items":crtItems,"filter":crtItem_filter}
    
    if request.POST.get("action")=="export":
        crtItem_filter = ProductFilter(request.POST, queryset=crtItems)
        today = timezone.now()
        print()
        context = {
            'today': today,
            'items': crtItem_filter.qs,
            'request': request,
            'qtyCnt':crtItem_filter.qs.aggregate(itemCount=Sum('crt_item_qty')),
            'totalCost':crtItem_filter.qs.aggregate(cost=Sum(ExpressionWrapper(F('crt_item_qty')*F("crt_item_price"),output_field=DecimalField()))),

        }
        pdf = render_to_pdf('Reports/report-pdf.html', context)
        
        if pdf:
            response = HttpResponse(pdf, content_type='application/pdf')
            filename = "Creative-Item-Report_%s.pdf" %(str(datetime.datetime.now()))
            content = "inline; filename=%s" %(filename)
            download = request.GET.get("download")
            if download:
                content = "attachment; filename=%s" %(filename)
            response['Content-Disposition'] = content
            return response

        return HttpResponse("Not found")

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
        


    else:
        return render(request, 'Reports/product-report.html',context)




























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
    
