from django.contrib import admin
from django.urls import path,include
from .views import *

app_name="Home"

urlpatterns = [
    path('',home,name="home"),
    path('creativestore/',creativestore,name="creativestore"),
    path('scrapyard/',scrapyard,name="scrapyard"),
    path('login/',login,name="login"),
    path('signup/',signup,name="signup"),
    path('shop/',include('Items.urls')),
    path('contact-us/', contactus, name="contactus"),
]
