from django.db import models
from django.core.validators import MaxValueValidator,MinValueValidator
from CustomAdmin.models import tbl_crt_subcategories,SubScrapCategory
from Authentication.models import User
from django.core.validators import validate_image_file_extension
import random,os
# Create your models here.
WEIGHT_CHOICES = (
    ("1", "Below 100g"),
    ("2", "Below 250g"),
    ("3", "Below 500g"),
    ("4", "Below 1kg"),
    ("5", "Below 5kg"),
)

ISSUE_TYPE_CHOICES = (
    (1, "Reported Creative Items"),
    (2, "Reported Scrap Items"),
    (3, "Reported Users Items"),

)

ISSUE_SUB_CHOICES = (
    (1, "Doesn't match product"),
    (2, "Missing/Incorrect information"),
    (3, "Offensive or adult content"),
    (4, "Is not clear"),
    (5, "Other"),

)
ISSUE_STATUS_CHOICES = (
    (1, "Pending"),
    (2, "Resolved"),
    (3, "Rejected"),

)

ITEM_STATUS = (
    ("INAPPROPRIATE","Inappropriate"),
    ("ACTIVE","Active"),
    ("INACTIVE","Inactive"),
    ("SOLD","Sold",)
)

def get_filename_ext(filepath):
    base_name = os.path.basename(filepath)
    name, ext = os.path.splitext(base_name)
    return name, ext

def product_photo(instance, filename):
    new_filename = random.randint(1,1000)
    name, ext = get_filename_ext(filename)
    final_filename = '{new_filename}{ext}'.format(new_filename=new_filename, ext=ext)
    return "crt-item-image/{final_filename}".format(final_filename=final_filename)


def scp_product_photo(instance, filename):
    new_filename = random.randint(1,1000)
    name, ext = get_filename_ext(filename)
    final_filename = '{new_filename}{ext}'.format(new_filename=new_filename, ext=ext)
    return "scp-item-image/{final_filename}".format(final_filename=final_filename)

class tbl_scrapitems(models.Model):
    scp_item_id = models.AutoField(primary_key=True, validators=[MaxValueValidator(9999999999)])
    scp_item_name = models.CharField(max_length=100, null=False, blank=False)
    scp_item_desc = models.TextField(blank=False, null=False)
    scp_item_price = models.DecimalField(blank=False, null=False, decimal_places=2, max_digits=10, validators=[MinValueValidator(1.00)])
    scp_item_qty = models.PositiveIntegerField(validators=[MaxValueValidator(999)], blank=False, null=False)
    scp_item_SKU = models.CharField(max_length=16, null=False, blank=False, unique=True)
    scp_item_status = models.CharField(max_length=20, null=False, blank=False, choices=ITEM_STATUS, default="ACTIVE")
    scp_created_on = models.DateTimeField(auto_now_add=True, null=False, blank=False)
    scp_last_modified = models.DateTimeField(auto_now_add=True, null=False, blank=False)
    scp_sub_category = models.ForeignKey(SubScrapCategory, on_delete=models.SET_DEFAULT, default=1)
    user = models.ForeignKey(User, on_delete=models.RESTRICT)
    username = models.ForeignKey(User, on_delete = models.DO_NOTHING,related_name="buyer_username",db_column="username",null=True,blank=True)

    def __str__(self):
        return self.scp_item_name
    
    def get_image_url(self):
        img = self.tbl_scrapimages_set.get(is_primary=True)
        if img:
            return img
        return img

class tbl_scrapimages(models.Model):
    scp_img_id = models.AutoField(primary_key=True, validators=[MaxValueValidator(99999)])
    scp_img_url = models.ImageField(max_length=150, null=True, upload_to=scp_product_photo, validators=[validate_image_file_extension])
    is_primary = models.BooleanField(default=False, null=False)
    scp_item = models.ForeignKey(tbl_scrapitems, on_delete=models.CASCADE)





class tbl_creativeitems_mst(models.Model):
    crt_item_id = models.AutoField(primary_key=True, validators=[MaxValueValidator(9999999999)])
    crt_item_name = models.CharField(max_length=100, null=False, blank=False)
    crt_item_desc = models.TextField(blank=False, null=False)
    crt_item_weight = models.CharField(max_length=1, choices=WEIGHT_CHOICES, blank=True, null=True)
    crt_item_height = models.DecimalField(decimal_places=2, max_digits=5,blank=True, null=True,default=0.0)
    crt_item_width = models.DecimalField(decimal_places=2, max_digits=5,blank=True,null=True,default=0.0)
    crt_item_price = models.DecimalField(blank=False, null=False, decimal_places=2, max_digits=10,
                                         validators=[MinValueValidator(1.00)])
    crt_item_qty = models.PositiveIntegerField(validators=[MaxValueValidator(999)], blank=False, null=False)
    crt_item_SKU = models.CharField(max_length=16, null=False, blank=False, unique=True)
    crt_item_status = models.CharField(max_length=20, null=False, blank=False, choices=ITEM_STATUS, default="ACTIVE")
    crt_created_on = models.DateTimeField(auto_now_add=True, null=False, blank=False)
    crt_last_modified = models.DateTimeField(auto_now_add=True, null=False, blank=False)
    crt_sub_category = models.ForeignKey(tbl_crt_subcategories,on_delete=models.SET_DEFAULT, default=1)
    user = models.ForeignKey(User, on_delete=models.RESTRICT)
    # scp_item = models.ForeignKey(tbl_scrapitems , null=True, blank=True, on_delete=models.SET_NULL, default=None)  # *** review on delete

    def __str__(self):
        return self.crt_item_name

    def get_image_url(self):
        
        img = self.tbl_crtimages_set.get(is_primary=True)
        if img:
            return img
        return img #None

    # def get_category(self):
    #     sub_category = self.tbl_crt_subcategories_set.get(crt_sub_category_id=self.crt_sub_category)
    #     category = sub_category.crt_category

# ITEM_SIZES = (
#     ("XS", "XS"),
#     ("S", "S"),
#     ("M", "M"),
#     ("L", "L"),
#     ("XL", "XL"),
#     ("XXL", "XXL"),
# )
#
#
#
# class tbl_creativeitems_details(models.Model):
#     crt_item_details_id = models.AutoField(primary_key=True, validators=[MaxValueValidator(9999999999)])
#     crt_item_color = models.CharField(max_length=7, null=False, blank=False)
#     crt_item_size = models.CharField(max_length=3, choices=ITEM_SIZES, null=True, blank=True)
#     crt_item_price = models.DecimalField(blank=False, null=False, decimal_places=2, max_digits=10, validators=[MinValueValidator(1.00)])  # *** set default price add minvalue
#     crt_item_qty = models.PositiveIntegerField(validators=[MaxValueValidator(999)],blank=False, null=False)
#     crt_item_SKU = models.CharField(max_length=16, null=False, blank=False, unique=True)
#     crt_item_status = models.CharField(max_length=20, null=False, blank=False, choices=ITEM_STATUS, default="ACTIVE")  # *** set default as inactive but in ppt default is active
#     crt_item = models.ForeignKey(tbl_creativeitems_mst, on_delete=models.CASCADE)
#
#     def __str__(self):
#         return self.crt_item_SKU


class tbl_crtimages(models.Model):
    crt_img_id = models.AutoField(primary_key=True, validators=[MaxValueValidator(99999)])
    crt_img_url = models.ImageField(max_length=150, null=True, upload_to=product_photo, validators=[validate_image_file_extension])
    is_primary = models.BooleanField(default=False, null=False)
    crt_item_details = models.ForeignKey(tbl_creativeitems_mst, on_delete=models.CASCADE)

    def __str__(self):
        return self.crt_item_details.crt_item_name


class Reviews(models.Model):
    review_id= models.AutoField(primary_key=True, validators=[MaxValueValidator(99999)])
    item_rating= models.DecimalField(decimal_places=1, max_digits=2,blank=True,null=True,default=0.0)
    item_review=models.TextField(blank=True, null=True)
    review_date=models.DateField(auto_now=True)
    crt_item=models.ForeignKey(tbl_creativeitems_mst, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.RESTRICT)





class Issues(models.Model):
    issue_id=models.AutoField(primary_key=True, validators=[MaxValueValidator(99999)])
    issue_type=models.PositiveIntegerField(choices=ISSUE_TYPE_CHOICES)
    issue_sub=models.PositiveIntegerField(choices=ISSUE_SUB_CHOICES)
    issue_msg = models.TextField(max_length=100,null=True,blank=True)
    issue_status = models.PositiveIntegerField(choices=ISSUE_STATUS_CHOICES,default=1)
    issue_date = models.DateTimeField(auto_now_add=True, null=False, blank=False)
    # crt_item = models.PositiveIntegerField(null=True,blank=True)
    # scp_item = models.PositiveIntegerField(null=True,blank=True)
    crt_item = models.ForeignKey(tbl_creativeitems_mst,on_delete=models.DO_NOTHING,null=True,blank=False)
    scp_item = models.ForeignKey(tbl_scrapitems,on_delete=models.DO_NOTHING,null=True,blank=False)
    reported_user = models.ForeignKey(User,on_delete=models.DO_NOTHING,null=True,blank=True,related_name='reportee')
    user=models.ForeignKey(User,on_delete=models.DO_NOTHING,related_name='reporter')
    
    class Meta:
        db_table = 'tbl_issues'

    def __str__(self):
        return self.issue_msg
