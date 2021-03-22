from django.urls import path, include,re_path
from django.conf.urls import url
from  .views import *
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
    path('reset-password/<slug:uidb64>/<slug:token>/',resetVerified, name='resetVerified'),
    path('new-password/',newPassword,name="newPassword"),
    path('new-password-done/',newPasswordDone,name="newPasswordDone"),
    path('logout/',logout,name="logout"),




    path('profile/<int:id>', profile, name="profile"),
    
    path('dashboard/', dashboard, name="dashboard"),
    path('dashboard/ajax/get-cities/<int:id>',getCities,name="getCities"),

    path('dashboard/product/creative/', creative_items, name="creative_items"),
    path('dashboard/product/scrap/', scrap_items, name="scrap_items"),

    path('dashboard/product/creative/add/', add_creative_product, name="add_creative_product"),
    path('dashboard/product/creative/add/<int:id>/', get_sub_category, name="get_sub_category"),
    # path('dashboard/product/creative/add/<str:action>/', add_creative_product, name="add_base_detail"),

    # path('dashboard/product/creative/add/item/<int:id>/', add_creative_product_detail, name="add_product_detail"),
    path('dashboard/upload-image/<int:id>/', upload_image, name="upload_image"),
   
    # path('dashboard/add-photo/<int:id>/', add_photo, name="add_photo"),

    path('dashboard/product/creative/edit/<int:id>/', edit_creative_product,name="edit_creative_product"),
    path('dashboard/product/creative/edit/<int:id>/ajax/set-primary/<int:imgid>',crtSetPrimary,name="setPrimary"),
    path('dashboard/product/creative/edit-creative-images/<int:id>/', edit_crt_images,name="edit_crt_images"),
    path('dashboard/product/creative/edit-creative-images/<str:action>/', edit_crt_images,name="add_crt_images"),
    path('dashboard/product/creative/remove-creative-images/<int:id>/', remove_crt_images,name="remove_crt_images"),

    path('dashboard/product/creative/remove-creative/<int:id>/', removeCrtItem,name="removeCrtItem"),





    path('dashboard/product/scrap/add/', add_scrap_product, name="add_scrap_product"),
    path('dashboard/product/scrap/add/<int:id>/', get_scp_sub_category, name="get_scp_sub_category"),

    path('dashboard/product/scrap/edit/<int:id>/', edit_scrap_product,name="edit_scrap_product"),
    path('dashboard/product/scrap/edit/<int:id>/ajax/set-primary/<int:imgid>',scpSetPrimary,name="setPrimary"),
    path('dashboard/product/scrap/edit-scrap-images/<int:id>/',edit_scp_images,name="edit_scp_images"),
    path('dashboard/product/scrap/edit-scrap-images/<str:action>/',edit_scp_images,name="add_scp_images"),
    path('dashboard/product/scrap/remove-scrap-images/<int:id>/',remove_scp_images,name="remove_scp_images"),

    path('dashboard/product/scrap/remove-scrap/<int:id>/', removeScpItem,name="removeScpItem"),


    path('dashboard/add-document/', add_document, name="add_document"),
    path('dashboard/profile/', dashboard_profile, name="dashboard_profile"),
    path('dashboard/profile/addAddress', addAddress, name="addAddress"),
    path('dashboard/profile/editAddress/<int:id>/', editAddress, name="editAddress"),
    path('dashboard/profile/delAddress/<int:id>/', delAddress, name="delAddress"),


    # path('dashboard/profile/ajax/get-cities/<int:id>',getCities,name="getCities"),
    

    path('dashboard/profile/ajax/set-default/<int:id>',setDefault,name="setDefault"),


    path('dashboard/profile/<str:action>', dashboard_profile, name="editProfileImage"),
    path('dashboard/profile/<str:action>', dashboard_profile, name="editProfileData"),

    

    # path('dashboard/profile/addAddress', addAddress, name="addAddress"),
    path('dashboard/profile/edit-document/', editDocument, name="editDocument"),
    path('dashboard/orders/creative/', order_creative, name="order_creative"),
    path('dashboard/orders/history/', order_history, name="order_history"),
    path('dashboard/orders/history/<str:action>', order_history, name="order_tab_history"),
    path('dashboard/orders/details/', order_details, name="order_details"),
    path('dashboard/orders/details/<int:id>/', order_details, name="order_details"),
    path('dashboard/payments/', dashboard_payments, name="payments"),
    path('dashboard/settings/', dashboard_settings, name="settings"),
    # path('photo-delete/<int:pk>/', product_photo_remove, name="photo_delete"),
    path('dashboard/settings/change-password', changePassword, name="changePassword"),
    path('dashboard/settings/deactive-account', deactiveAccount, name="deactiveAccount"),

    #path('photo-delete/<int:pk>/', product_photo_remove, name="photo_delete"),
    # path('photo-upload/', BasicUploadView, name='basic_upload'),

    ######REPORTS######
    path('', include('UserReports.urls')),

    ######CHARTS######
    path('', include('Charts.urls')),


    
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)