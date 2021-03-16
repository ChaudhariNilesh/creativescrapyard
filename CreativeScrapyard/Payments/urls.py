from django.urls import path
from .views import initiate_payment, callback,clearSession
app_name="Payments"

urlpatterns = [
    path('pay/', initiate_payment, name='pay'),
    path('callback/', callback, name='callback'),
    path('ajax/clear-sess/', clearSession, name='clearSession'),

]
