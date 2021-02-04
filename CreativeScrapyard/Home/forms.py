from django import forms
from .models import *


class QueryForm(forms.Form):
    model = Query
    fields = ('name','email','query_subject','query_message')