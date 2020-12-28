from django.urls import path, include
from .views import *

app_name = "Authentication"

urlpatterns = [
    path('profile/', profile, name="profile"),
    path('dashboard/', dashboard, name="dashboard"),
    path('dashboard/product/creative/', creative_items, name="creative_items"),
    path('dashboard/product/creative/add', add_creative_product, name="add_creative_product"),
    path('dashboard/add-document/', add_document, name="add_document"),
    path('dashboard/profile/', dashboard_profile, name="dashboard_profile"),
    path('dashboard/orders/creative/', order_creative, name="order_creative"),
    path('dashboard/orders/history/', order_history, name="order_history"),
    path('dashboard/orders/details/', order_details, name="order_details"),
    path('dashboard/settings/', settings, name="settings"),
]
