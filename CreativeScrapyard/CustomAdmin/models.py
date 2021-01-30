from django.db import models
from django.core.validators import MaxValueValidator

# Create your models here.
class tbl_crt_categories(models.Model):
    crt_category_id =  models.AutoField(primary_key=True,validators=[MaxValueValidator(99999)])
    crt_category_name = models.CharField(max_length=40)

    class Meta:
        db_table = 'tbl_crt_categories'

    def __str__(self):
        return self.crt_category_name

class tbl_crt_subcategories(models.Model):
    crt_sub_category_id =  models.AutoField(primary_key=True,validators=[MaxValueValidator(99999)])
    crt_sub_category_name = models.CharField(max_length=40)
    crt_category = models.ForeignKey(tbl_crt_categories, on_delete=models.CASCADE)

    class Meta:
        db_table = "tbl_crt_subcategories"

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
    
