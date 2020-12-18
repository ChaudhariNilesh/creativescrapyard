
from django.contrib import admin
from django.urls import path,include
from .views import *

app_name="Home"

urlpatterns = [
    path('',home,name="home"),
    path('shop/',include('Items.urls')),

]
