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
    date_joined = models.DateTimeField(auto_now_add=True, null=False, blank=False, db_column="created_on")
    
    def __str__(self):
        return self.username

class Profile(models.Model):
    user_id = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    bio = models.TextField(max_length=200, null=True, blank=True)
    user_image = models.ImageField(upload_to='user_photo', null=True)
    #user_mobile = models.CharField(max_length=10, unique=True, null=False, blank=False)
    user_gender = models.CharField(max_length=1, choices=GENDER_TYPE, null=False)
    is_verified = models.BooleanField(null=False, default=False)
    user_rating = models.DecimalField(null=True,decimal_places=1, max_digits=2)

    def __str__(self):
        return self.user_id.username


class Photo(models.Model):
    title = models.CharField(max_length=255, blank=True)
    file = models.ImageField(upload_to='photos/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
