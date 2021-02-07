from django import forms
from .models import *
from Home.validate import *


class QueryForm(forms.ModelForm):
    class Meta:

        model = Query
        fields = ('first_name','last_name','email','query_subject','query_message')

    # def clean(self):
    #     cleaned_data = self.cleaned_data
    #     email = cleaned_data.get('email',None)
    #     first_name = cleaned_data.get('first_name',None)
    #     context={}
     
    #     if not first_name.isalpha():
    #         context["first_name"]="Invalid Name"
    #     else:
    #         context["first_name"]=""
    #     if not email.endswith("gmail.com"):
    #         context["email"]="Invalid Email."
    #     else:
    #         context["email"]=""

    #     raise forms.ValidationError(context)

        # context = validate(email=email, fname=first_name)
        # #print(context)
        # if context:
        #     error_dict=context
        #     print(error_dict)
        #     raise forms.ValidationError(message=dict(context))
        #return cleaned_data