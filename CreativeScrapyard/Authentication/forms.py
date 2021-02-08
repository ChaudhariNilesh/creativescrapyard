from django import forms
from .models import *

#
# class CustomUserForm(forms.ModelForm):
#     class Meta:
#         models = CustomUser
#         fields = ('username','bio','full_name', 'user_mobile', 'user_gender')


# class UserForm(forms.ModelForm):
    
#     class Meta:
#         model = User
#         fields = ("first_name","last_name","username","email","password")

# class ProfileForm(forms.ModelForm):
    
#     class Meta:
#         model = Profile
#         fields = ("user_gender",)



class PhotoForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = ('file', )