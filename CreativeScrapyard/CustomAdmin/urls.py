from django.urls import path,include
from .views import *

app_name="CustomAdmin"

urlpatterns = [
    path('',adminindex,name="adminindex"),
    path('login/',login,name="login"),
    # path('logout/',logout,name="logout"),
    path('users/',users,name="users"),
    path('change-password/',changePassword,name="changePassword"),
    path('admin-account/',adminAccount,name="adminAccount"),
    path('logout/',logout,name="logout"),
    
    path('buyers/',buyers,name="buyers"),
    path('sellers/',sellers,name="sellers"),
    path('verify-users/',verifyusers,name="verifyusers"),
    
    ######CREATIVE CATEGORIES######
    path('creative-categories/',creativeCat,name="creativeCat"),   
    path('creative-categories/<int:id>/',creativeCat,name="loadSubCrtCat"),
    path('creative-categories/<str:action>/',creativeCat,name="addMainCrtCat"),
    path('creative-categories/<int:id>/<str:action>/',creativeCat,name="CrtCatAction"),

    ######SCRAP CATEGORIES######
    path('scrap-categories/',scrapCat,name="scrapCat"),
    path('scrap-categories/<int:id>/',scrapCat,name="loadSubScpCat"),
    path('scrap-categories/<str:action>/',scrapCat,name="addMainScpCat"),
    path('scrap-categories/<int:id>/<str:action>/',scrapCat,name="ScpCatAction"),


    path('creativeitems/',creativeitems,name="creativeitems"),    
    path('scrapitems/',scrapitems,name="scrapitems"),

    path('allorders',allorders,name='allorders'),
    path('orderdetails/<int:id>',orderdetails,name='orderdetails'), # 

    path('allorderdetails/',allorderdetails,name='allorderdetails'),
    path('allorderdetails/tab/<str:action>/',allorderdetails,name='allorderdetailsTab'),#Order Detail tab
    ######AJAX######
    path('ajax/view-details/',viewDets,name="viewDets"),
    path('ajax/documents/',docuDownload,name="docuDownload"),
    path('ajax/verify/',verifyChk,name="verifyChk"),






    path('badges/',badges,name="badges"),
]