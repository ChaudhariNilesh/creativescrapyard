from django.urls import path
from .views import *

app_name = "UserReports"

urlpatterns = [
  ################### CRT/SCP ITEM ###################
  path('crt-item-report/', productReports, name='productReports'),
  path('crt-item-report/<str:export>', productReports, name='productReports'),
  

  path('scp-item-report/', scpItemsReports, name='scpItemsReports'),
  path('scp-item-report/<str:export>', scpItemsReports, name='scpItemsReports'),

 
  ################### ORDER ###################
  path('order-report/', orderReports, name='orderReports'),
  path('order-report/<str:export>', orderReports, name='orderReports'),

  
]