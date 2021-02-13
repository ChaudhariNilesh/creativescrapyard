from django.urls import path, include,re_path
from django.conf.urls import url
from .views import *
from django.conf import settings
from django.conf.urls.static import static

app_name = "Authentication"

urlpatterns = [
    path('login/',UserLogin,name="login"),
    path('signup/',signup,name="signup"),
    path('email-verification-sent/',EmailverificationSent,name="EmailverificationSent"),
    path('activate/<slug:uidb64>/<slug:token>/',activateAccount, name='activateAccount'),
    # path('activate-done/',activateAccountDone, name='activateAccountDone'),
    path('password-reset-link/',passwordReset,name="passwordReset"),
    path('password-reset-done/',passwordResetLink,name="passwordResetLink"),
    path('new-password/',newPassword,name="newPassword"),
    path('new-password-done/',newPasswordDone,name="newPasswordDone"),
    path('logout/',logout,name="logout"),




    path('profile/', profile, name="profile"),
    path('dashboard/', dashboard, name="dashboard"),
    path('dashboard/product/creative/', creative_items, name="creative_items"),
    path('dashboard/product/scrap/', scrap_items, name="scrap_items"),
    path('dashboard/product/creative/add', add_creative_product, name="add_creative_product"),
    path('dashboard/product/creative/add/get-sub-crt-cat/<int:pk>', add_creative_product, name="get_crt_sub_cat"),
    path('dashboard/add-document/', add_document, name="add_document"),
    path('dashboard/profile/', dashboard_profile, name="dashboard_profile"),
    path('dashboard/profile/addAddress', addAddress, name="addAddress"),
    path('dashboard/profile/edit-document/', editDocument, name="editDocument"),
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