from django.urls import path, include
from .views import *

app_name = "Authentication"

urlpatterns = [
    path('profile/', profile, name="profile"),
    path('dashboard/', dashboard, name="dashboard"),
    path('dashboard/add-product/', add_product, name="add_product"),
    path('dashboard/add-document/', add_document, name="add_document"),
]
