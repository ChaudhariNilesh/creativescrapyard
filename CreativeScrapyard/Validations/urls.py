from django.urls import path

from .views import *

app_name = 'Validations'

urlpatterns = [
    path('ajax/validate/signup/',validationSignUpForm,name="validationSignUpForm")
]

