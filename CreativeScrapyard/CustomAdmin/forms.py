from .models import MainCreativeCategory,SubCreativeCategory,MainScrapCategory,SubScrapCategory
from django import forms

class MainCreativeCategoryForm(forms.ModelForm):
    class Meta:
        model = MainCreativeCategory
        fields = ('crt_category_name',)

    def clean(self):
        cleaned_data = self.cleaned_data
       
        crt_category_name = cleaned_data.get('crt_category_name', None)
        
        if len(crt_category_name) < 5:
            raise forms.ValidationError("Category Name is Too Short!!")

        return cleaned_data
        

class SubCreativeCategoryForm(forms.ModelForm):
    class Meta:
        model = SubCreativeCategory
        fields = ('crt_sub_category_name',)

class MainScrapCategoryForm(forms.ModelForm):
    class Meta:
        model = MainScrapCategory
        fields = ('scp_category_name',)


class SubScrapCategoryForm(forms.ModelForm):
    class Meta:
        model = SubScrapCategory
        fields = ('scp_sub_category_name',)


