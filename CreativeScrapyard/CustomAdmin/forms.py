from .models import tbl_crt_categories,tbl_crt_subcategories,MainScrapCategory,SubScrapCategory
from Authentication.models import User
from django import forms
import re
class AdminForm(forms.ModelForm):

    class Meta:
        model = User
        fields=('first_name','last_name',)
        exclude = ('username','email',)
        
    
    def clean_first_name(self):
        cleaned_data=self.cleaned_data

        first_name = cleaned_data.get("first_name",None)
        #last_name = cleaned_data.get("last_name",None)

        if not first_name.isalpha():
            self.add_error("first_name",forms.ValidationError('Invalid first name. Only Alphabets are accepted.' ,code='invalid'))
        #if not last_name.isalpha():
         #   self.add_error("last_name",forms.ValidationError('Invalid last name only. Alphabets are accepted.' ,code='invalid'))

        return first_name
   
    def clean_last_name(self):
        cleaned_data=self.cleaned_data

        last_name = cleaned_data.get("last_name",None)

        if not last_name.isalpha():
              self.add_error("last_name",forms.ValidationError('Invalid last name. Only Alphabets are accepted.' ,code='invalid'))

        return last_name    
    

class MainCreativeCategoryForm(forms.ModelForm):
    class Meta:
        model = tbl_crt_categories
        fields = ('crt_category_name',)

    def clean(self):
        cleaned_data = self.cleaned_data
       
        crt_category_name = cleaned_data.get('crt_category_name', None)
        cat = bool(re.match('[a-zA-Z\s]+$', crt_category_name))
        if not cat:
            raise forms.ValidationError("Creative Category Name is invalid.")

        return cleaned_data
      
        

class SubCreativeCategoryForm(forms.ModelForm):
    class Meta:
        model = tbl_crt_subcategories
        fields = ('crt_sub_category_name',)
    
    def clean(self):
        cleaned_data = self.cleaned_data
       
        crt_sub_category_name = cleaned_data.get('crt_sub_category_name', None)
        cat = bool(re.match('[a-zA-Z\s]+$', crt_sub_category_name))
        if not cat:
            raise forms.ValidationError("Creative Sub-Category Name is invalid.")

        return cleaned_data      

class MainScrapCategoryForm(forms.ModelForm):
    class Meta:
        model = MainScrapCategory
        fields = ('scp_category_name',)

    def clean(self):
        cleaned_data = self.cleaned_data
       
        scp_category_name = cleaned_data.get('scp_category_name', None)
        cat = bool(re.match('[a-zA-Z\s]+$', scp_category_name))
        if not cat:
            raise forms.ValidationError("Scrap Category Name is invalid.")

        return cleaned_data 


class SubScrapCategoryForm(forms.ModelForm):
    class Meta:
        model = SubScrapCategory
        fields = ('scp_sub_category_name',)

    def clean(self):
        cleaned_data = self.cleaned_data
       
        scp_sub_category_name = cleaned_data.get('scp_sub_category_name', None)
        cat = bool(re.match('[a-zA-Z\s]+$', scp_sub_category_name))
        if not cat:
            raise forms.ValidationError("Scrap Sub-Category Name is invalid.")

        return cleaned_data  



