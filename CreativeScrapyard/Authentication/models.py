from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator

gender_type = (
    ('F', 'Female'),
    ('M', 'Male'),
)


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

# Create your models here.
class Photo(models.Model):
    title = models.CharField(max_length=255, blank=True)
    file = models.ImageField(upload_to='photos/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
