from django.db import models
from django.core.validators import MaxValueValidator
# Create your models here.
class Query(models.Model):
    query_id = models.AutoField(primary_key=True,validators=[MaxValueValidator(9999999999)])
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=256, null=False)
    query_subject = models.CharField(max_length=50, null=False)
    query_message = models.CharField(max_length=500, null=True)
    query_status = models.CharField(max_length=80,default="Pending")
    query_date = models.DateTimeField(auto_now_add=True, null=False, blank=False)

    def __str__(self):
        return self.email