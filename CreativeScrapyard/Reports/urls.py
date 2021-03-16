from django.urls import path
from .views import *
app_name = "Reports"
# from model_report import report
# report.autodiscover()

urlpatterns = [
  ################### CRT/SCP ITEM ###################
  path('crt-item-report/', productReports, name='productReports'),
  path('crt-item-report/<str:export>', productReports, name='productReports'),
  # path('crt-item-report/<str:by>/<str:search>/<str:export>', productReports, name='productReports'),

  path('scp-item-report/', scpItemsReports, name='scpItemsReports'),
  path('scp-item-report/<str:export>', scpItemsReports, name='scpItemsReports'),

  ################### USER ###################
  path('user-report/', userReports, name='userReports'),
  path('user-report/<str:export>', userReports, name='userReports'),
  
  ################### ORDER ###################
  path('order-report/', orderReports, name='orderReports'),
  path('order-report/<str:export>', orderReports, name='orderReports'),

  # path('generate-reports/',reports,name='reports')
]