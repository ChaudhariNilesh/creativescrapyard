from django.urls import path
from django.contrib import admin
from django.urls import path,include
from .views import *

app_name = 'Charts'

urlpatterns = [
    path("charts/<int:type>",charts,name="charts"),
    path("charts/categorywise-items",catItemCharts,name="catItemCharts"),
    path("charts/categorywise-orders",catOrdCharts,name="catOrdCharts"),
    path("charts/item-wise",itemsCharts,name="itemsCharts"),
    path("charts/user-wise",userCharts,name="userCharts"),
    path("charts/month-wise-orders",monOrds,name="monOrds"),
    path("charts/month-wise-sales",monSales,name="monSales"),



    

    

    
]
