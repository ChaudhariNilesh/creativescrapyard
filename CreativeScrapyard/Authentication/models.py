from django.db import models
from django.contrib.auth.models import AbstractUser

gender_type = (
    ('F', 'Female'),
    ('M', 'Male'),
)

# class CustomUser(AbstractUser):
#     user_id =


# Create your models here.
class Photo(models.Model):
    title = models.CharField(max_length=255, blank=True)
    file = models.ImageField(upload_to='photos/')
    uploaded_at = models.DateTimeField(auto_now_add=True)