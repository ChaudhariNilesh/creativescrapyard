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
    
    path('creative-categories/',creativeCat,name="creativeCat"),
    path('creativeitems/',creativeitems,name="creativeitems"),
    path('scrap-categories/',scrapCat,name="scrapCat"),
    path('scrapitems/',scrapitems,name="scrapitems"),
    
    #AJAX
    path('ajax/view-details/',viewDets,name="viewDets"),
    path('ajax/documents/',docuDownload,name="docuDownload"),
    path('ajax/verify/',verifyChk,name="verifyChk"),





    path('badges/',badges,name="badges"),
]