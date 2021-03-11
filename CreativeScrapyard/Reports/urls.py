from django.urls import path
from .views import *
app_name = "Reports"
# from model_report import report
# report.autodiscover()

urlpatterns = [
  path('crt-item-report/', productReports, name='productReports'),
  path('crt-item-report/<str:export>', productReports, name='productReports'),
  path('crt-item-report/<str:by>/<str:search>/<str:export>', productReports, name='productReports'),
  
  path('generate-reports/',reports,name='reports')
]