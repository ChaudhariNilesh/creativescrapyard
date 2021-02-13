from django import forms
from .models import *
import re

#
# class CustomUserForm(forms.ModelForm):
#     class Meta:
#         models = CustomUser
#         fields = ('username','bio','full_name', 'user_mobile', 'user_gender')


# class UserForm(forms.ModelForm):
    
#     class Meta:
#         model = User
#         fields = ("first_name","last_name","username","email","password")

# class ProfileForm(forms.ModelForm):
    
#     class Meta:
#         model = Profile
#         fields = ("user_gender",)

class EditUserDocument(forms.ModelForm):

    class Meta:
        model=Documents
        fields=("acc_no","acc_name","bank_name","IFSC_code")
        exclude=("pan_no","pan_name","pan_img_url")

    def clean_acc_no(self):
        acc_no=self.cleaned_data.get("acc_no",None)

        if not acc_no.isdigit() or len(acc_no) > 20 or len(acc_no) < 9:
            self.add_error("acc_no",forms.ValidationError('Enter Valid Account Number.'))
        
        return acc_no
    
    def clean_acc_name(self):
        acc_name=self.cleaned_data.get("acc_name",None)

        if not  bool(re.match('[a-zA-Z\s]+$', acc_name)):
            self.add_error("acc_name",forms.ValidationError("Account Name Shouldn't Contain Digit"))

        return acc_name

    def clean_bank_name(self):
        bank_name=self.cleaned_data.get("bank_name",None)

        if bank_name=="none":
            self.add_error("bank_name",forms.ValidationError("Select Bank Name"))

        return bank_name

    def clean_IFSC_code(self):
        IFSC_code=self.cleaned_data.get("IFSC_code",None)

        if not len(IFSC_code)==11 and not IFSC_code[0:4].isalpha() and not IFSC_code[4]=="0" and not IFSC_code[5:11].isdigit():
            self.add_error("IFSC_code",forms.ValidationError("Enter Valid IFSC code"))

        return IFSC_code





class UserDocument(forms.ModelForm):

    class Meta:
        model=Documents
        fields=("acc_no","acc_name","bank_name","IFSC_code","pan_no","pan_name","pan_img_url")

    def clean_acc_no(self):
        acc_no=self.cleaned_data.get("acc_no",None)

        if not acc_no.isdigit() or len(acc_no) > 20 or len(acc_no) < 9:
            self.add_error("acc_no",forms.ValidationError('Enter Valid Account Number.'))
        
        return acc_no
    
    def clean_acc_name(self):
        acc_name=self.cleaned_data.get("acc_name",None)

        if not  bool(re.match('[a-zA-Z\s]+$', acc_name)):
            self.add_error("acc_name",forms.ValidationError("Account Name Shouldn't Contain Digit"))

        return acc_name

    def clean_bank_name(self):
        bank_name=self.cleaned_data.get("bank_name",None)

        if bank_name=="none":
            self.add_error("bank_name",forms.ValidationError("Select Bank Name"))

        return bank_name

    # def clean_bank_name(self):
    #     bank_name=self.cleaned_data.get()

    #     if not bank_name.isalpha():
    #         self.add_error("bank_name",forms.ValidationError("Bank Name Shouldn't Contain Digit"))

    #     return bank_name

    def clean_IFSC_code(self):
        IFSC_code=self.cleaned_data.get("IFSC_code",None)

        if not len(IFSC_code)==11 and not IFSC_code[0:4].isalpha() and not IFSC_code[4]=="0" and not IFSC_code[5:11].isdigit():
            self.add_error("IFSC_code",forms.ValidationError("Enter Valid IFSC code"))

        return IFSC_code




    def clean_pan_no(self):
        pan_no=self.cleaned_data.get("pan_no",None)

        if not len(pan_no)==10 or not pan_no[0:5].isalpha() or not pan_no[5:10].isdigit():
            self.add_error("pan_no",forms.ValidationError("Enter Valid Pan Card No."))

        return pan_no

    def clean_pan_name(self):
        pan_name=self.cleaned_data.get("pan_name",None)

        if not pan_name.isalpha():
            self.add_error("pan_name",forms.ValidationError("Pan Name Shouldn't Contain Digit"))
        
        return pan_name


class AddressForm(forms.ModelForm):
    
    class Meta:
        model = Address
        fields = ("person_name","contact_no","type","line1","line2","landmark","city_id","state_id","pincode")

    def clean_person_name(self):
        cleaned_data=self.cleaned_data
        person_name=cleaned_data.get("person_name",None)

        if not bool(re.match('[a-zA-Z\s]+$', person_name)):
            self.add_error("person_name",forms.ValidationError('Invalid person name. Only Alphabets are accepted.' ,code='invalid'))
        
        return person_name
    
    def clean_contact_no(self):
        cleaned_data=self.cleaned_data
        contact_no=cleaned_data.get("contact_no",None)

        if not contact_no.isdigit() or not len(contact_no)==10:
            self.add_error("contact_no",forms.ValidationError('Invalid contact number. Enter only ten digit number.' ,code='invalid'))

        return contact_no
    
    def clean_type(self):
        type=self.cleaned_data.get("type",None)

        if type=="none":
            self.add_error("type",forms.ValidationError('Please Select The Address Type'))
        
        return type

    

    def clean_line1(self):
        line1=self.cleaned_data.get("line1",None)

        if len(line1)==0:
            self.add_error("line1",forms.ValidationError('Please Enter Address Line 1'))

        return line1
    
    def clean_line2(self):
        line2=self.cleaned_data.get("line2",None)

        if len(line2)==0:
            self.add_error("line2",forms.ValidationError('Please Enter Address Line 2'))

        return line2

    def clean_pincode(self):
        pincode=self.cleaned_data.get("pincode",None)

        if not len(pincode)==6 or not pincode.isdigit():
            self.add_error("pincode",forms.ValidationError("Please Enter Valid Pincode"))
        
        return pincode
    



class PhotoForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = ('file', )

