from django import forms
from django.forms import fields
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
        if not bool(re.match('[a-zA-Z0-9\.\,\s]+$', crt_item_desc)):
            self.add_error("crt_item_desc",
                           forms.ValidationError('Invalid item description. Only alphabets and numeric are accepted.',
                                                 code='invalid'))

        return crt_item_desc

    def clean_crt_item_weight(self):
        cleaned_data = self.cleaned_data

        crt_item_weight = cleaned_data.get('crt_item_weight', "")
        # print("===>", crt_item_weight)
        options = ['1', '2', '3', '4', '5']
        if not crt_item_weight in options:
            self.add_error("crt_item_weight", forms.ValidationError('some is wrong', code='invalid'))

        return crt_item_weight

    def clean_crt_item_height(self):
        cleaned_data = self.cleaned_data
        crt_item_height = cleaned_data.get('crt_item_height', "")
        if crt_item_height:
            try:
                # print("form ==> ", crt_item_height)
                crt_item_height = int(crt_item_height)
                if crt_item_height < 1:
                    self.add_error("crt_item_height", forms.ValidationError('Invalid item height.', code='invalid'))
            except :
                pass

        return crt_item_height

    def clean_crt_item_width(self):
        cleaned_data = self.cleaned_data
        crt_item_width = cleaned_data.get('crt_item_width', "")
        if crt_item_width:
            try:
                crt_item_width = int(crt_item_width)
                if crt_item_width < 1:
                    self.add_error("crt_item_width", forms.ValidationError('Invalid item width.', code='invalid'))
            except:
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
    crt_img_url_1 = forms.ImageField(allow_empty_file="False",required=True)
    crt_img_url_2 = forms.ImageField(allow_empty_file="True",required=False)
    crt_img_url_3 = forms.ImageField(allow_empty_file="True",required=False)
    crt_img_url_4 = forms.ImageField(allow_empty_file="True",required=False)
    crt_img_url_5 = forms.ImageField(allow_empty_file="True",required=False)
    crt_img_url_6 = forms.ImageField(allow_empty_file="True",required=False)

    def clean_crt_img_url_1(self):
        cleaned_data = self.cleaned_data
        crt_img_url_1 = cleaned_data.get('crt_img_url_1', None)
        # print(crt_img_url_1)
        if crt_img_url_1:
            allowedSize = round((crt_img_url_1.size/1024))
            # validate_image_file_extension(crt_img_url_1)                
            if allowedSize > 5048:
                self.add_error("crt_img_url_1",forms.ValidationError('Maximum 5 MB image size is allowed.' ,code='invalid'))

        return crt_img_url_1

    def clean_crt_img_url_2(self):
        cleaned_data = self.cleaned_data
        crt_img_url_2 = cleaned_data.get('crt_img_url_2', None)
        # print(crt_img_url_2)
        if crt_img_url_2:
            allowedSize = round((crt_img_url_2.size/1024))
            # validate_image_file_extension(crt_img_url_2)                
            if allowedSize > 5048:
                self.add_error("crt_img_url_2",forms.ValidationError('Maximum 5 MB image size is allowed.' ,code='invalid'))

        return crt_img_url_2
    
    def clean_crt_img_url_3(self):
        cleaned_data = self.cleaned_data
        crt_img_url_3 = cleaned_data.get('crt_img_url_3', None)
        # print(crt_img_url_3)
        if crt_img_url_3:
            allowedSize = round((crt_img_url_3.size/1024))
            # validate_image_file_extension(crt_img_url_3)                
            if allowedSize > 5048:
                self.add_error("crt_img_url_3",forms.ValidationError('Maximum 5 MB image size is allowed.' ,code='invalid'))

        return crt_img_url_3

    def clean_crt_img_url_4(self):
        cleaned_data = self.cleaned_data
        crt_img_url_4 = cleaned_data.get('crt_img_url_4', None)
        # print(crt_img_url_4)
        if crt_img_url_4:
            allowedSize = round((crt_img_url_4.size/1024))
            # validate_image_file_extension(crt_img_url_4)                
            if allowedSize > 5048:
                self.add_error("crt_img_url_4",forms.ValidationError('Maximum 5 MB image size is allowed.' ,code='invalid'))

        return crt_img_url_4

    def clean_crt_img_url_5(self):
        cleaned_data = self.cleaned_data
        crt_img_url_5 = cleaned_data.get('crt_img_url_5', None)
        # print(crt_img_url_5)
        if crt_img_url_5:
            allowedSize = round((crt_img_url_5.size/1024))
            # validate_image_file_extension(crt_img_url_5)                
            if allowedSize > 5048:
                self.add_error("crt_img_url_5",forms.ValidationError('Maximum 5 MB image size is allowed.' ,code='invalid'))

        return crt_img_url_5

    def clean_crt_img_url_6(self):
        cleaned_data = self.cleaned_data
        crt_img_url_6 = cleaned_data.get('crt_img_url_6', None)
        # print(crt_img_url_6)
        if crt_img_url_6:
            allowedSize = round((crt_img_url_6.size/1024))
            # validate_image_file_extension(crt_img_url_6)                
            if allowedSize > 5048:
                self.add_error("crt_img_url_6",forms.ValidationError('Maximum 5 MB image size is allowed.' ,code='invalid'))

        return crt_img_url_6
    


class EditCrtImage(forms.ModelForm):
    class Meta:
        model=tbl_crtimages
        fields=("crt_img_url",)




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
        if not bool(re.match('[a-zA-Z0-9\.\,\s]+$', scp_item_desc)):
            self.add_error("scp_item_desc", forms.ValidationError(
                'Invalid item description. Only alphabets and numeric are accepted.', code='invalid'))

        return scp_item_desc


class tbl_scpimages_form(forms.Form):
    # class Meta:
    #     fields = ('scp_img_url_1','scp_img_url_2','scp_img_url_3','scp_img_url_4','scp_img_url_5','scp_img_url_6')
    scp_img_url_1 = forms.ImageField(allow_empty_file="False",required=True)
    scp_img_url_2 = forms.ImageField(allow_empty_file="True",required=False)
    scp_img_url_3 = forms.ImageField(allow_empty_file="True",required=False)
    scp_img_url_4 = forms.ImageField(allow_empty_file="True",required=False)
    scp_img_url_5 = forms.ImageField(allow_empty_file="True",required=False)
    scp_img_url_6 = forms.ImageField(allow_empty_file="True",required=False)

    def clean_scp_img_url_1(self):
        cleaned_data = self.cleaned_data
        scp_img_url_1 = cleaned_data.get('scp_img_url_1', None)
        # print(scp_img_url_1)
        if scp_img_url_1:
            allowedSize = round((scp_img_url_1.size/1024))
            # validate_image_file_extension(scp_img_url_1)                
            if allowedSize > 5048:
                self.add_error("scp_img_url_1",forms.ValidationError('Maximum 5 MB image size is allowed.' ,code='invalid'))

        return scp_img_url_1

    def clean_scp_img_url_2(self):
        cleaned_data = self.cleaned_data
        scp_img_url_2 = cleaned_data.get('scp_img_url_2', None)
        # print(scp_img_url_2)
        if scp_img_url_2:
            allowedSize = round((scp_img_url_2.size/1024))
            # validate_image_file_extension(scp_img_url_2)                
            if allowedSize > 5048:
                self.add_error("scp_img_url_2",forms.ValidationError('Maximum 5 MB image size is allowed.' ,code='invalid'))

        return scp_img_url_2
    
    def clean_scp_img_url_3(self):
        cleaned_data = self.cleaned_data
        scp_img_url_3 = cleaned_data.get('scp_img_url_3', None)
        # print(scp_img_url_3)
        if scp_img_url_3:
            allowedSize = round((scp_img_url_3.size/1024))
            # validate_image_file_extension(scp_img_url_3)                
            if allowedSize > 5048:
                self.add_error("scp_img_url_3",forms.ValidationError('Maximum 5 MB image size is allowed.' ,code='invalid'))

        return scp_img_url_3

    def clean_scp_img_url_4(self):
        cleaned_data = self.cleaned_data
        scp_img_url_4 = cleaned_data.get('scp_img_url_4', None)
        # print(scp_img_url_4)
        if scp_img_url_4:
            allowedSize = round((scp_img_url_4.size/1024))
            # validate_image_file_extension(scp_img_url_4)                
            if allowedSize > 5048:
                self.add_error("scp_img_url_4",forms.ValidationError('Maximum 5 MB image size is allowed.' ,code='invalid'))

        return scp_img_url_4

    def clean_scp_img_url_5(self):
        cleaned_data = self.cleaned_data
        scp_img_url_5 = cleaned_data.get('scp_img_url_5', None)
        # print(scp_img_url_5)
        if scp_img_url_5:
            allowedSize = round((scp_img_url_5.size/1024))
            # validate_image_file_extension(scp_img_url_5)                
            if allowedSize > 5048:
                self.add_error("scp_img_url_5",forms.ValidationError('Maximum 5 MB image size is allowed.' ,code='invalid'))

        return scp_img_url_5

    def clean_scp_img_url_6(self):
        cleaned_data = self.cleaned_data
        scp_img_url_6 = cleaned_data.get('scp_img_url_6', None)
        # print(scp_img_url_6)
        if scp_img_url_6:
            allowedSize = round((scp_img_url_6.size/1024))
            # validate_image_file_extension(scp_img_url_6)                
            if allowedSize > 5048:
                self.add_error("scp_img_url_6",forms.ValidationError('Maximum 5 MB image size is allowed.' ,code='invalid'))

        return scp_img_url_6
    


class EditScpImage(forms.ModelForm):
    class Meta:
        model=tbl_scrapimages
        fields=("scp_img_url",)


# class tbl_scrapimages_form(forms.ModelForm):
#     class Meta:
#         model = tbl_scrapimages
#         fields = ('scp_img_url',)

class ReportIssueForm(forms.ModelForm):
    class Meta:
        model = Issues
        fields=("issue_type","issue_sub","issue_msg",)

    def clean_issue_msg(self):
        cleaned_date = self.cleaned_data
        issue_msg = cleaned_date.get("issue_msg",False)
        
        if issue_msg:
            if not bool(re.match('[a-zA-Z0-9\&\\\.\,\s]+$',issue_msg)):
                self.add_error("issue_msg",forms.ValidationError("No special symbols are allowed in the message field.",code="invalid"))
        
        return issue_msg            
