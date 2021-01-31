from django import forms
from .models import *


class tbl_orders_mst_form(forms.ModelForm):
    class Meta:
        model = tbl_orders_mst