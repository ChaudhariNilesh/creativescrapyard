from django import forms
from .models import *

#
# class CustomUserForm(forms.ModelForm):
#     class Meta:
#         models = CustomUser
#         fields = ('username','bio','full_name', 'user_mobile', 'user_gender')


    

class PhotoForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = ('file', )