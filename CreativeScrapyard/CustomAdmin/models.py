from django.db import models
from django.core.validators import MaxValueValidator

# Create your models here.
class MainCreativeCategory(models.Model):
    crt_category_id =  models.AutoField(primary_key=True,validators=[MaxValueValidator(99999)])
    crt_category_name = models.CharField(max_length=40)

    def __str__(self):
        return self.crt_category_name

class SubCreativeCategory(models.Model):
    crt_sub_category_id =  models.AutoField(primary_key=True,validators=[MaxValueValidator(99999)])
    crt_sub_category_name = models.CharField(max_length=40)
    crt_category = models.ForeignKey(MainCreativeCategory, on_delete=models.CASCADE)

    def __str__(self):
        return self.crt_sub_category_name


class MainScrapCategory(models.Model):
    scp_category_id =  models.AutoField(primary_key=True,validators=[MaxValueValidator(99999)])
    scp_category_name = models.CharField(max_length=40)

    def __str__(self):
        return self.scp_category_name

class SubScrapCategory(models.Model):
    scp_sub_category_id =  models.AutoField(primary_key=True,validators=[MaxValueValidator(99999)])
    scp_sub_category_name = models.CharField(max_length=40)
    scp_category = models.ForeignKey(MainScrapCategory, on_delete=models.CASCADE)

    def __str__(self):
        return self.scp_sub_category_name
    
