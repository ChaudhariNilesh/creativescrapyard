from django import forms
from .models import *
from django.core.validators import validate_image_file_extension
import re
import requests
#
# class CustomUserForm(forms.ModelForm):
#     class Meta:
#         models = CustomUser
#         fields = ('username','bio','full_name', 'user_mobile', 'user_gender')


class EditUserFormData(forms.ModelForm):
    
    class Meta:
        model = User
        fields = ("first_name","last_name")
    
    def clean_first_name(self):
        cleaned_data=self.cleaned_data

        first_name = cleaned_data.get("first_name",None)

        if not first_name.isalpha():
            self.add_error("first_name",forms.ValidationError('Invalid first name only. Alphabets are accepted.' ,code='invalid'))
        return first_name

   
    def clean_last_name(self):
        cleaned_data=self.cleaned_data

        last_name = cleaned_data.get("last_name",None)

        if not last_name.isalpha():
              self.add_error("last_name",forms.ValidationError('Invalid last name only. Alphabets are accepted.' ,code='invalid'))

        return last_name   

class EditProfileImage(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ("user_image",)
    
    def clean_user_image(self):
        cleaned_data=self.cleaned_data
        #print(cleaned_data)
        user_image = cleaned_data.get("user_image",False)
        # print()
        if user_image:
            allowedSize = round((user_image.size/1024))
            validate_image_file_extension(user_image)
            if allowedSize > 2048:
                self.add_error("user_image",forms.ValidationError('Maximum 2 MB image size is allowed.' ,code='invalid'))

        return cleaned_data   

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
            self.add_error("acc_name",forms.ValidationError("Account Name Shouldn't Contain Digit or Special Characters"))

        return acc_name

    def clean_bank_name(self):
        bank_name=self.cleaned_data.get("bank_name",None)

        if bank_name=="none":
            self.add_error("bank_name",forms.ValidationError("Select Bank Name"))

        return bank_name

    def clean_IFSC_code(self):
        IFSC_code=self.cleaned_data.get("IFSC_code",None)

        if not len(IFSC_code)==11 or not IFSC_code[0:4].isalpha() or not IFSC_code[4]=="0" or not IFSC_code[5:11].isdigit():
            self.add_error("IFSC_code",forms.ValidationError("Enter Valid IFSC code"))

        return IFSC_code





class EditProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ("bio","user_gender",)
        exclude = ("user_image",)
            
    def clean_bio(self):
        cleaned_data=self.cleaned_data
        #print(cleaned_data)
        bio = cleaned_data.get("bio",None)
        #print(bio)
        try:
            if bio:
                res = bool(re.match('[a-zA-Z0-9\s]+$', bio))
                if not res:
                    self.add_error("bio",forms.ValidationError('Invalid bio. Only Alphabet letter (a-z) and numbers (0-9) are accepted' ,code='invalid'))
        except: 
            pass
        
        return cleaned_data           

class UserDocument(forms.ModelForm):

    class Meta:
        model=Documents
        fields=("acc_no","acc_name","IFSC_code","pan_no","pan_name","bank_name","pan_img_url",)

    def clean_acc_no(self):
        acc_no=self.cleaned_data.get("acc_no",None)

        if not acc_no.isdigit() or len(acc_no) < 9 or len(acc_no) > 20  :
            self.add_error("acc_no",forms.ValidationError('Enter Valid Account Number.'))
        
        return acc_no
    
    def clean_acc_name(self):
        acc_name=self.cleaned_data.get("acc_name",None)

        if not bool(re.match('[a-zA-Z\s]+$',acc_name)):
            self.add_error("acc_name",forms.ValidationError("Account Name Shouldn't Contain Digit or Any Special Characters."))

        return acc_name

    def clean_bank_name(self):
        bank_name=self.cleaned_data.get("bank_name",None)

        if bank_name=="none":
            self.add_error("bank_name",forms.ValidationError("Select Bank Name"))

        return bank_name

    # def clean_bank_name(self):
    #     bank_name=self.cleaned_data.get("bank_name",None)

    #     if not bool(re.match('[a-zA-Z\s]+$',bank_name)):
    #         self.add_error("bank_name",forms.ValidationError("Bank Name Shouldn't Contain Digit"))

    #     return bank_name

    def clean_IFSC_code(self):
        IFSC_code=self.cleaned_data.get("IFSC_code",None)

        if not len(IFSC_code)==11 or not IFSC_code[0:4].isalpha() or not IFSC_code[4]=="0" or not IFSC_code[5:11].isdigit():
            self.add_error("IFSC_code",forms.ValidationError("Enter Valid IFSC code"))

        return IFSC_code

    def clean_pan_no(self):
        pan_no=self.cleaned_data.get("pan_no",None)

        if not len(pan_no)==10 or not pan_no[0:5].isalpha() or not pan_no[5:9].isdigit() or not pan_no[9].isalpha():
            self.add_error("pan_no",forms.ValidationError("Enter Valid Pan Card No."))

        return pan_no

    def clean_pan_name(self):
        pan_name=self.cleaned_data.get("pan_name",None)

        if not bool(re.match('[a-zA-Z\s]+$',pan_name)):
            self.add_error("pan_name",forms.ValidationError("Pan Name Shouldn't Contain Digit or Any Special Characters."))
        
        return pan_name
    
    def clean_pan_img_url(self):
        cleaned_data=self.cleaned_data
        #print(cleaned_data) {"name":value}
        pan_img_url = cleaned_data.get("pan_img_url",False)
        allowedSize = round((pan_img_url.size/1024))
        if pan_img_url:
            validate_image_file_extension(pan_img_url)                
            if allowedSize > 2048:
                self.add_error("pan_img_url",forms.ValidationError('Maximum 2 MB image size is allowed.' ,code='invalid'))
        
        return pan_img_url


class AddressForm(forms.ModelForm):
    
    class Meta:
        model = Address
        fields = ("person_name","contact_no","type","line1","line2","pincode","landmark","city","state")

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

        if not bool(re.match('^[\.a-zA-Z0-9,\s ]+$',line1)):
            self.add_error("line1",forms.ValidationError('Please enter correct address Line 1'))

        return line1
    
    def clean_line2(self):
        line2=self.cleaned_data.get("line2",None)

        if not bool(re.match('^[\.a-zA-Z0-9,\s ]+$',line2)):
            self.add_error("line2",forms.ValidationError('Please enter correct address Line 2'))

        return line2

    def clean_landmark(self):
        landmark=self.cleaned_data.get("landmark",None)
        #print(landmark)
        try:
            if landmark :
                if not bool(re.match('^[\.a-zA-Z0-9,\s ]+$',landmark)):
                    self.add_error("landmark",forms.ValidationError('Only alphabets and number are accepted.'))
        except :
            pass
            
        return landmark
        
            

    def clean_pincode(self):
        pincode=self.cleaned_data.get("pincode",None)
        response = requests.get('https://api.postalpincode.in/pincode/'+pincode)
        isvalidpincode = response.json()
        # print(isvalidpincode[0]['Status'])
        if not len(pincode)==6 or not pincode.isdigit() or isvalidpincode[0]['Status']=="Error":
        # if not len(pincode)==6 or not pincode.isdigit():

            self.add_error("pincode",forms.ValidationError("Please Enter Valid Pincode"))
        
        return pincode

    # def clean_state(self):
    #     state=self.cleaned_data.get("state",None)


    #     stateExist = States.objects.filter(state_id=state.state_id).exists()
    #     if not stateExist:
    #         self.add_error("state",forms.ValidationError("Please select your state."))
    #     # print(state.state_id)
    #     if not state:
    #         #print("not selec")
    #         self.add_error("state",forms.ValidationError("Please select your state."))
    #     return state.state_id
    
    # def clean_city(self):
    #     city=self.cleaned_data.get("city",None)


    #     cityExist = Cities.objects.filter(city_id=city.city_id).exists()
    #     cityObj = Cities.objects.filter(city_id=city.city_id).values()
    #     if not cityExist:
    #         self.add_error("city",forms.ValidationError("Please select your city."))
    #     # print(city.city)
    #     if not city:
    #         # print("not selec")
    #         self.add_error("city",forms.ValidationError("Please select your city."))
    #     return city
    



class PhotoForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = ('file', )

