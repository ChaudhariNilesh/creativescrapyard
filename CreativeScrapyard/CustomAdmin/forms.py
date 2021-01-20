from .models import MainCreativeCategory,SubCreativeCategory
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
