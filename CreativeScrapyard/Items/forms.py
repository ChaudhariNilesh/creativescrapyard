from django import forms
from .models import *


class tbl_creativeitems_mst_form(forms.ModelForm):
    class Meta:
        model = tbl_creativeitems_mst
        fields = ('crt_item_name', 'crt_item_desc',)
    #     print("heloFomr")

    # def clean_crt_items_name(self,*args):
    #
    #     print(dict(args[0])["crt_item_name"])
    #     name=dict(args[0])["crt_item_name"]
    #
    #     if len(*name) < 5 :
    #         print("HelInvalid")
    #         return False
    #     else:
    #         print("Nikul pagal ")
    #         return True
    # return crt_items_name[0].upper() + crt_items_name[1:].lower()


class tbl_creativeitems_details_form(forms.ModelForm):
    class Meta:
        model = tbl_creativeitems_details
        fields = (
        'crt_item_color', 'crt_item_size', 'crt_item_price', 'crt_item_qty', 'crt_item_weight', 'crt_item_height',
        'crt_item_width', 'crt_item_status')
