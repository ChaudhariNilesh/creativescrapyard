from django.urls import path,include
from .views import *

app_name="CustomAdmin"

urlpatterns = [
    path('',adminindex,name="adminindex"),
    path('login/',login,name="login"),
    # path('logout/',logout,name="logout"),
    path('users/',users,name="users"),
]