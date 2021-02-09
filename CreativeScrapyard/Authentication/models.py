from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator

GENDER_TYPE = (
    ('F', 'Female'),
    ('M', 'Male'),
)

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
    user_id = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    bio = models.TextField(max_length=200, null=True, blank=True)
    user_image = models.ImageField(upload_to='user_photo', null=True)
    user_mobile = models.CharField(max_length=10, unique=True, null=False, blank=False)
    user_gender = models.CharField(max_length=1, choices=GENDER_TYPE, null=False)
    is_verified = models.BooleanField(null=False, default=False)
    user_rating = models.DecimalField(decimal_places=1, max_digits=2)
    
    class Meta:
        db_table = 'tbl_profile_mst'

    def __str__(self):
        return self.user_id

class Documents(models.Model):
    doc_id =models.AutoField(primary_key=True, validators=[MaxValueValidator(99999)])
    user_id = models.OneToOneField(User, on_delete=models.CASCADE)
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
        return self.doc_id

class States(models.Model):
    state_id=models.AutoField(primary_key=True,validators=[MaxValueValidator(99999)])
    state_name=models.CharField(max_length=30,blank=False,null=False)

    class Meta:
        db_table = 'tbl_states'

    def __str__(self):
        return self.state_id


class Cities(models.Model):
    city_id=models.AutoField(primary_key=True,validators=[MaxValueValidator(99999)])
    city_name=models.CharField(max_length=30,blank=False,null=False)
    state_id=models.ForeignKey(States,on_delete=models.CASCADE)

    class Meta:
        db_table = 'tbl_cities'

    def __str__(self):
        return self.city_id

class Address(models.Model):
    address_id=models.AutoField(primary_key=True, validators=[MaxValueValidator(99999)])
    user_id=models.ForeignKey(User,on_delete=models.CASCADE)
    person_name=models.CharField(max_length=20,null=False,blank=False)
    contact_no=models.CharField(max_length=10,null=False,blank=False)
    pincode=models.CharField(max_length=6,null=False,blank=False)
    line1=models.TextField(max_length=100,null=False,blank=False)
    line2=models.TextField(max_length=100,null=False,blank=False)
    landmark=models.TextField(max_length=50,null=False,blank=False)
    is_default=models.BooleanField(null=False, default=False)
    type=models.CharField(max_length=6,null=False,blank=False)
    city_id=models.ForeignKey(Cities,on_delete=models.DO_NOTHING)
    state_id=models.ForeignKey(States,on_delete=models.DO_NOTHING)
    
    class Meta:
        db_table = 'tbl_address'

    def __str__(self):
        return self.address_id


class Photo(models.Model):
    title = models.CharField(max_length=255, blank=True)
    file = models.ImageField(upload_to='photos/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
