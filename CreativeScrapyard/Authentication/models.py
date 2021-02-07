from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.core.validators import MaxValueValidator, MinValueValidator

gender_type = (
    ('F', 'Female'),
    ('M', 'Male'),
)

class BaseUser(AbstractBaseUser):

    ''' base user class '''
    USERNAME_FIELD='email'
    email = models.CharField(max_length=256, unique=True, null=False, blank=False)
    first_name = models.CharField(max_length=100, null=False, blank=False)
    last_name = models.CharField(max_length=100, null=False, blank=False)

    @property
    def is_normal_user(self):
        try:
            return self.normal_user and True
        except:
            return False

    @property
    def is_admin_user(self):
        try:
             return self.admin_user and True
        except:
             return False
    

class NormalUser(models.Model):

    ''' normal user, extends BaseUser class '''

    base_user = models.OneToOneField('BaseUser', related_name='normal_user',on_delete=models.CASCADE)
    email = models.CharField(max_length=256, unique=True, null=False, blank=False)
        

class AdminUser(models.Model):

    ''' admin user, extends BaseUser class '''

    base_user = models.OneToOneField('BaseUser', related_name='admin_user',on_delete=models.CASCADE)
    email = models.CharField(max_length=256, unique=True, null=False, blank=False)

# class CustomUser(AbstractUser):
#     user_id = models.PositiveIntegerField(primary_key=True, validators=[MaxValueValidator(99999)])
#     username = models.CharField(max_length=50, unique=True, null=False, blank=False)
#     bio = models.TextField(max_length=200, null=True, blank=True)
#     full_name = models.CharField(max_length=200, null=False, blank=False)
#     # user_image = models.ImageField()
#     # user_email = models.EmailField(max_length=256, unique=True, null=False, blank=False)
#     user_mobile = models.CharField(max_length=10, unique=True, null=False, blank=False)
#     # user_password = models
#     user_gender = models.CharField(max_length=1, Choices=gender_type, null=False)
#     user_status = models.BooleanField(null=False)
#     is_verified = models.BooleanField(null=False)
#     created_on = models.DateTimeField(auto_now_add=True, null=False, blank=False)
#     user_rating = models.DecimalField(decimal_places=1, max_digits=2)

class Photo(models.Model):
    title = models.CharField(max_length=255, blank=True)
    file = models.ImageField(upload_to='photos/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
