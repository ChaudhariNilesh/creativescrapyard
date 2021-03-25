from django.contrib import admin
from django.urls import path,include
from .views import *

app_name="Home"

urlpatterns = [
    path('',home,name="home"),
    path('',include('Validations.urls')),    
    path('creativestore/',creativestore,name="creativestore"),
    # path('creativestore/',creativestore,name="crtpricefilter"),
    # path('creativestore/search/',creativestore,name="creativestore"),
    path('creativestore/sort/<str:sort>',creativestore,name="creativestoresort"),
    
    path('creativestore/<str:type>/<int:id>/',creativestore,name="creativestore"),
    path('creativestore/<str:type>/<int:id>/<str:sort>',creativestore,name="creativestore"),
    

    # path('creativestore/search/',creativestore,name="creativestoreSearch"),
    
    
    path('scrapyard/',scrapyard,name="scrapyard"),
    path('scrapyard/<str:type>/<int:id>/',scrapyard,name="scrapyard"),
    path('scrapyard/sort/<str:sort>',scrapyard,name="scrapyardsort"),
    path('scrapyard/',scrapyard,name="scppricefilter"),

    path('achievers/',achievers,name="achievers"),

    path('shop/',include('Items.urls')),

    path('contact-us/', contactus, name="contactus"),
    path('about-us/', aboutus, name="aboutus"),    
    path('contact-scrapseller/',sendContactDetails,name="sendContactDetails"),

    # path('accounts',include('Authentication.urls')),






]
