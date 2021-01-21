from .models import MainCreativeCategory,SubCreativeCategory,MainScrapCategory,SubScrapCategory
from django import forms

class MainCreativeCategoryForm(forms.ModelForm):
    class Meta:
        model = MainCreativeCategory
        fields = ('crt_category_name',)
        widgets={
            'crt_category_name' : forms.TextInput(attrs={'class':'form-control'}),
        }

class SubCreativeCategoryForm(forms.ModelForm):
    class Meta:
        model = SubCreativeCategory
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

