from django.contrib import admin
from django.urls import path,include
from .views import *

app_name="Home"

urlpatterns = [
    path('',home,name="home"),
    path('creativestore/',creativestore,name="creativestore"),
    path('scrapyard/',scrapyard,name="scrapyard"),
    path('achievers/',achievers,name="achievers"),
    path('login/',login,name="login"),
    path('signup/',signup,name="signup"),
    path('shop/',include('Items.urls')),
    path('contact-us/', contactus, name="contactus"),
    path('about-us/', aboutus, name="aboutus"),    
    path('accounts',include('Authentication.urls')),
    path('password-reset-link/',passwordReset,name="passwordReset"),
    path('password-reset-done/',passwordResetLink,name="passwordResetLink"),
    path('new-password/',newPassword,name="newPassword"),
    path('new-password-done/',newPasswordDone,name="newPasswordDone"),




]
