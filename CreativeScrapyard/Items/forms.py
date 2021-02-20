from django import forms
from .models import *
from django.forms.models import modelformset_factory
import re


class tbl_creativeitems_mst_form(forms.ModelForm):
    class Meta:
        model = tbl_creativeitems_mst
        fields = ('crt_item_name', 'crt_item_desc', 'crt_item_weight', 'crt_item_height', 'crt_item_width',
                  'crt_item_price', 'crt_item_qty')

    def clean_crt_item_name(self):
        cleaned_data = self.cleaned_data

        crt_item_name = cleaned_data.get('crt_item_name', None)
        if not bool(re.match('[a-zA-Z0-9\s]+$', crt_item_name)):
            self.add_error("crt_item_name",
                           forms.ValidationError('Invalid item name. Only alphabets and numeric are accepted.',
                                                 code='invalid'))

        return crt_item_name

    def clean_crt_item_desc(self):
        cleaned_data = self.cleaned_data

        crt_item_desc = cleaned_data.get('crt_item_desc', None)
        if not bool(re.match('[a-zA-Z0-9\s]+$', crt_item_desc)):
            self.add_error("crt_item_desc",
                           forms.ValidationError('Invalid item description. Only alphabets and numeric are accepted.',
                                                 code='invalid'))

        return crt_item_desc

    def clean_crt_item_weight(self):
        cleaned_data = self.cleaned_data

        crt_item_weight = cleaned_data.get('crt_item_weight', None)
        # print("===>", crt_item_weight)
        options = ['1', '2', '3', '4', '5']
        if not crt_item_weight in options:
            self.add_error("crt_item_weight", forms.ValidationError('some is wrong', code='invalid'))

        return crt_item_weight

    def clean_crt_item_height(self):
        cleaned_data = self.cleaned_data
        crt_item_height = cleaned_data.get('crt_item_height', None)

        try:
            print("form ==> ", crt_item_height)
            crt_item_height = int(crt_item_height)
            if crt_item_height != None and crt_item_height < 1:
                self.add_error("crt_item_height", forms.ValidationError('Invalid item height.', code='invalid'))
        except :
            pass
        if crt_item_height == None:
            self.add_error("crt_item_height", forms.ValidationError('empty', code='valid'))
        return crt_item_height

    def clean_crt_item_width(self):
        cleaned_data = self.cleaned_data
        crt_item_width = cleaned_data.get('crt_item_width', None)
        try:
            crt_item_width = int(crt_item_width)
            if crt_item_width != None and int(crt_item_width) < 1:
                self.add_error("crt_item_width", forms.ValidationError('Invalid item width.', code='invalid'))
        except:

            if crt_item_width == None:
                self.add_error("crt_item_width", forms.ValidationError('empty', code='valid'))
            pass



        return crt_item_width

#
# class tbl_creativeitems_details_form(forms.ModelForm):
#     class Meta:
#         model = tbl_creativeitems_details
#         fields = ('crt_item_color', 'crt_item_size', 'crt_item_price', 'crt_item_qty')


class tbl_crtimages_form(forms.Form):
    # class Meta:
    #     fields = ('crt_img_url_1','crt_img_url_2','crt_img_url_3','crt_img_url_4','crt_img_url_5','crt_img_url_6')
    crt_img_url_1 = forms.ImageField(allow_empty_file="False")
    crt_img_url_2 = forms.ImageField(allow_empty_file="True")
    crt_img_url_3 = forms.ImageField(allow_empty_file="True")
    crt_img_url_4 = forms.ImageField(allow_empty_file="True")
    crt_img_url_5 = forms.ImageField(allow_empty_file="True")
    crt_img_url_6 = forms.ImageField(allow_empty_file="True")




class tbl_scrapitems_form(forms.ModelForm):
    class Meta:
        model = tbl_scrapitems
        fields = ('scp_item_name', 'scp_item_desc', 'scp_item_price', 'scp_item_qty',)

    def clean_scp_item_name(self):
        cleaned_data = self.cleaned_data

        scp_item_name = cleaned_data.get('scp_item_name', None)
        if not bool(re.match('[a-zA-Z0-9\s]+$', scp_item_name)):
            self.add_error("scp_item_name",
                           forms.ValidationError('Invalid item name. Only alphabets and numeric are accepted.',
                                                 code='invalid'))

        return scp_item_name

    def clean_scp_item_desc(self):
        cleaned_data = self.cleaned_data

        scp_item_desc = cleaned_data.get('scp_item_desc', None)
        if not bool(re.match('[a-zA-Z0-9\s]+$', scp_item_desc)):
            self.add_error("scp_item_desc", forms.ValidationError(
                'Invalid item description. Only alphabets and numeric are accepted.', code='invalid'))

        return scp_item_desc

class tbl_scrapimages_form(forms.ModelForm):
    class Meta:
        model = tbl_scrapimages
        fields = ('scp_img_url',)