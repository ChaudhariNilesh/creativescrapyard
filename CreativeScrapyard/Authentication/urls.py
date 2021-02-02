from django.urls import path, include
from .views import *
from django.conf import settings
from django.conf.urls.static import static

app_name = "Authentication"

urlpatterns = [
    path('profile/', profile, name="profile"),
    path('dashboard/', dashboard, name="dashboard"),
    path('dashboard/product/creative/', creative_items, name="creative_items"),
    path('dashboard/product/scrap/', scrap_items, name="scrap_items"),
    path('dashboard/product/creative/add', add_creative_product, name="add_creative_product"),
    path('dashboard/product/creative/add/get-sub-crt-cat/<int:pk>', add_creative_product, name="get_crt_sub_cat"),
    path('dashboard/add-document/', add_document, name="add_document"),
    path('dashboard/profile/', dashboard_profile, name="dashboard_profile"),
    path('dashboard/orders/creative/', order_creative, name="order_creative"),
    path('dashboard/orders/history/', order_history, name="order_history"),
    path('dashboard/orders/history/<str:action>', order_history, name="order_tab_history"),
    path('dashboard/orders/details/', order_details, name="order_details"),
    path('dashboard/payments/', dashboard_payments, name="payments"),
    path('dashboard/settings/', dashboard_settings, name="settings"),
    path('photo-delete/<int:pk>/', product_photo_remove, name="photo_delete"),
    # path('photo-upload/', BasicUploadView, name='basic_upload'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)