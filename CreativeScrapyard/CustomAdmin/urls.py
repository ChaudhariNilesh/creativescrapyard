from django.urls import path,include
from .views import *

app_name="CustomAdmin"

urlpatterns = [

    path('',adminindex,name="adminindex"),
    path('login/',AdminLogin,name="login"),
    path('users/',users,name="users"),
    path('change-password/',changePassword,name="changePassword"),
    path('admin-account/',adminAccount,name="adminAccount"),
    path('logout/',logout,name="logout"),
    
    path('buyers/',buyers,name="buyers"),
    path('sellers/',sellers,name="sellers"),
    path('verify-users/',verifyusers,name="verifyusers"),
    path('verify-users/<str:tab>',verifyusers,name="verifyusers"),


    
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

    path('allorders/',allorders,name='allorders'),
    path('orderdetails/<int:id>',orderdetails,name='orderdetails'), # 

    path('allorderdetails/',allorderdetails,name='allorderdetails'),
    path('allorderdetails/<str:action>/',allorderdetails,name='allorderdetailsTab'),#Order Detail tab
    
    ######PAYMENT#####
    path('payment/',payment,name='payment'),

    ######AJAX######
    path('ajax/view-details/',viewDets,name="viewDets"),
    path('ajax/documents/',docuDownload,name="docuDownload"),
    path('ajax/verify/',verifyChk,name="verifyChk"),


    ######BADGES######
    path('badges/',badges,name="badges"),
    path('add-badges/',addBadges,name="addBadges"),
    path('assign-badges/',assignBadges,name="assignBadges"), 
    path('del-badge/',delBadge,name="delBadge"),
    path('remove-assigned/',removeAssignedBadge,name="removeAssignedBadge"),   


    ######QUERIES######
    path('query/',queries,name="query"),
    path('issues/',issues,name="issues"),

    ######MAIL######
    path('send-mail/',sendmail,name="sendmail"),
    path('send-mail/<str:action>',sendmail,name="sendmail"),
    path('reply-query/<int:id>',replyQry,name="replyQry"),



]