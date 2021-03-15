from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator, validate_image_file_extension
import random
import os
from .models import *
from Items.models import *


GENDER_TYPE = (
    ('F', 'Female'),
    ('M', 'Male'),
)
# BANK_NAME = (
#     (1, 'State Bank of India'),
#     (2, 'Bank of Baroda'),
#     (3, 'ICICI Bank'),
#     (4, 'HDFC Bank'),
#     (5, 'Bank of India'),
#     (6, 'Axis Bank'),
# )


def get_filename_ext(filepath):
    base_name = os.path.basename(filepath)
    name, ext = os.path.splitext(base_name)
    return name, ext

def user_photo(instance, filename):
    new_filename = random.randint(1,1000)
    name, ext = get_filename_ext(filename)
    final_filename = '{new_filename}{ext}'.format(new_filename=new_filename, ext=ext)
    return "users/{final_filename}".format(final_filename=final_filename)

class User(AbstractUser):
    user_id = models.AutoField(primary_key=True, validators=[MaxValueValidator(99999)])
    username = models.CharField(max_length=50, unique=True, null=False, blank=False)
    first_name = models.CharField(max_length=100, null=False, blank=False )
    last_name = models.CharField(max_length=100, null=False, blank=False )
    email = models.EmailField(max_length=256, unique=True, null=False, blank=False, db_column="user_email")
    password = models.CharField(max_length=158, null=False, blank=False, db_column="user_password")
    is_active = models.BooleanField(null=False, blank=False, default=True, db_column="user_status")
    date_joined = models.DateTimeField( auto_now_add=True, null=False, blank=False, db_column="created_on")

    class Meta:
        db_table = 'tbl_user_mst'

    def __str__(self):
        return self.username


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    bio = models.TextField(max_length=200, null=True, blank=True,default="")
    user_image = models.ImageField(upload_to=user_photo,null=True,default=None)
    #user_mobile = models.CharField(max_length=10, unique=True, null=False, blank=False)
    user_gender = models.CharField(max_length=1, choices=GENDER_TYPE, null=False)
    is_verified = models.BooleanField(null=False, default=False)
    user_rating = models.DecimalField(null=True,decimal_places=1, max_digits=2,blank=True,default=0.0)

    def __str__(self):
        return self.user.username


class Documents(models.Model):
    doc_id =models.AutoField(primary_key=True, validators=[MaxValueValidator(99999)])
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    acc_no=models.CharField(max_length=20,null=False,blank=False)
    acc_name=models.CharField(max_length=50,null=False,blank=False)
    bank_name=models.CharField(max_length=50,null=False,blank=False)
    IFSC_code=models.CharField(max_length=11,null=False,blank=False)
    pan_no=models.CharField(max_length=10,null=False,blank=False)
    pan_name=models.CharField(max_length=25,null=False,blank=False)
    pan_img_url = models.ImageField(upload_to='doc_photo', null=True)

    class Meta:
        db_table = 'tbl_user_documents'

    def __str__(self):
        return self.user.username

class States(models.Model):
    state_id=models.AutoField(primary_key=True,validators=[MaxValueValidator(99999)])
    state_name=models.CharField(max_length=30,blank=False,null=False)

    class Meta:
        db_table = 'tbl_states'

    def __str__(self):
        return self.state_name


class Cities(models.Model):
    city_id=models.AutoField(primary_key=True,validators=[MaxValueValidator(99999)])
    city_name=models.CharField(max_length=30,blank=False,null=False)
    state=models.ForeignKey(States,on_delete=models.CASCADE)

    class Meta:
        db_table = 'tbl_cities'

    def __str__(self):
        return self.city_name

class Address(models.Model):
    address_id=models.AutoField(primary_key=True, validators=[MaxValueValidator(99999)])
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    person_name=models.CharField(max_length=20,null=False,blank=False)
    contact_no=models.CharField(max_length=10,null=False,blank=False)
    pincode=models.CharField(max_length=6,null=False,blank=False)
    line1=models.TextField(max_length=100,null=False,blank=False)
    line2=models.TextField(max_length=100,null=False,blank=False)
    landmark=models.TextField(max_length=50,null=True,blank=True)
    is_default=models.BooleanField(null=False, default=False)
    type=models.CharField(max_length=6,null=False,blank=False)
    city=models.ForeignKey(Cities,on_delete=models.DO_NOTHING)
    state=models.ForeignKey(States,on_delete=models.DO_NOTHING)
    
    class Meta:
        db_table = 'tbl_address'

    def __str__(self):
        return self.person_name



class Photo(models.Model):
    title = models.CharField(max_length=255, blank=True)
    file = models.ImageField(upload_to='photos/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

# class Review(models.Model):
#     review_id=models.AutoField(primary_key=True, validators=[MaxValueValidator(9999999999)])
#     user=models.ForeignKey(User,on_delete=models.CASCADE)
#     item_rating = models.DecimalField(null=False,decimal_places=1, max_digits=2,blank=False)
#     item_review=models.TextField(max_length=500,null=True,blank=True)
#     review_date=models.DateTimeField(auto_now_add=True, null=False, blank=False)
#     tbl_creativeitems_details_id=models.ForeignKey(tbl_creativeitems_details,on_delete=models.CASCADE)
    
#     class Meta:
#         db_table = 'tbl_review'

#     def __str__(self):
#         return self.user.username
