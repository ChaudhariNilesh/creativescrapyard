from .models import tbl_crt_categories,tbl_crt_subcategories,MainScrapCategory,SubScrapCategory
from django import forms

class MainCreativeCategoryForm(forms.ModelForm):
    class Meta:
        model = tbl_crt_categories
        fields = ('crt_category_name',)
        widgets={
            'crt_category_name' : forms.TextInput(attrs={'class':'form-control'}),
        }

class SubCreativeCategoryForm(forms.ModelForm):
    class Meta:
        model = tbl_crt_subcategories
        fields = ('crt_sub_category_name',)
        widgets={
            'crt_sub_category_name' : forms.TextInput(attrs={'class':'form-control'}),
        }

class MainScrapCategoryForm(forms.ModelForm):
    class Meta:
        model = MainScrapCategory
        fields = ('scp_category_name',)
        widgets={
            'scp_category_name' : forms.TextInput(attrs={'class':'form-control'}),
        }

class SubScrapCategoryForm(forms.ModelForm):
    class Meta:
        model = SubScrapCategory
        fields = ('scp_sub_category_name',)
        widgets={
            'scp_sub_category_name' : forms.TextInput(attrs={'class':'form-control'}),
        }

