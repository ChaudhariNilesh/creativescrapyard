from django import forms
from .models import *
from django.core.validators import validate_image_file_extension
import re

#
# class CustomUserForm(forms.ModelForm):
#     class Meta:
#         models = CustomUser
#         fields = ('username','bio','full_name', 'user_mobile', 'user_gender')


class EditUserFormData(forms.ModelForm):
    
    class Meta:
        model = User
        fields = ("first_name","last_name")
    
    def clean_first_name(self):
        cleaned_data=self.cleaned_data

        first_name = cleaned_data.get("first_name",None)

        if not first_name.isalpha():
            self.add_error("first_name",forms.ValidationError('Invalid first name only. Alphabets are accepted.' ,code='invalid'))
        return first_name

   
    def clean_last_name(self):
        cleaned_data=self.cleaned_data

        last_name = cleaned_data.get("last_name",None)

        if not last_name.isalpha():
              self.add_error("last_name",forms.ValidationError('Invalid last name only. Alphabets are accepted.' ,code='invalid'))

        return last_name   

class EditProfileImage(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ("user_image",)
    
    def clean_user_image(self):
        cleaned_data=self.cleaned_data
        #print(cleaned_data)
        user_image = cleaned_data.get("user_image",False)
    
        if user_image:
            validate_image_file_extension(user_image)
                #self.add_error("last_name",forms.ValidationError('Invalid last name only. Alphabets are accepted.' ,code='invalid'))

        return cleaned_data   

class EditProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ("bio","user_gender",)
        exclude = ("user_image",)
            
    def clean_bio(self):
        cleaned_data=self.cleaned_data
        #print(cleaned_data)
        bio = cleaned_data.get("bio",False)
        #print(bio)
        res = bool(re.match('[a-zA-Z0-9\s]+$', bio))
        if not res:
            self.add_error("bio",forms.ValidationError('Invalid bio. Only Alphabet letter (a-z) and numbers (0-9) are accepted' ,code='invalid'))

        return cleaned_data           


class PhotoForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = ('file', )