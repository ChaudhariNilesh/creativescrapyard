from django.db import models
from django.core.validators import MaxValueValidator,MinValueValidator
from CustomAdmin.models import tbl_crt_subcategories,SubScrapCategory
from django.core.validators import validate_image_file_extension


# Create your models here.

WEIGHT_CHOICES = (
    ("1", "Below 100g"),
    ("2", "Below 250g"),
    ("3", "Below 500g"),
    ("4", "Below 1kg"),
    ("5", "Below 5kg"),
)

class tbl_creativeitems_mst(models.Model):
    crt_item_id = models.AutoField(primary_key=True, validators=[MaxValueValidator(9999999999)])
    crt_item_name = models.CharField(max_length=100, null=False, blank=False)
    crt_item_desc = models.TextField(blank=False, null=False)
    crt_item_weight = models.CharField(max_length=1, choices=WEIGHT_CHOICES, blank=True, null=True,)
    crt_item_height = models.DecimalField(decimal_places=2, max_digits=5)
    crt_item_width = models.DecimalField(decimal_places=2, max_digits=5)
    crt_created_on = models.DateTimeField(auto_now_add=True, null=False, blank=False)
    crt_last_modified = models.DateTimeField(auto_now_add=True, null=False, blank=False)
    crt_sub_category = models.ForeignKey(tbl_crt_subcategories,on_delete=models.SET_DEFAULT, default=1)   # *** set default sub-category as other
    # user = models.ForeignKey( , on_delete=models.RESTRICT)
    # scp_item = models.ForeignKey( , null=True, blank=True, on_delete=models.SET_NULL)  # *** review on delete

    def __str__(self):
        return self.crt_item_name

ITEM_SIZES = (
    ("XS", "XS"),
    ("S", "S"),
    ("M", "M"),
    ("L", "L"),
    ("XL", "XL"),
    ("XXL", "XXL"),
)

ITEM_STATUS = (
    ("INAPPROPRIATE","Inappropriate"),
    ("ACTIVE","Active"),
    ("INACTIVE","Inactive"),
    ("SOLD","Sold",)
)

class tbl_creativeitems_details(models.Model):
    crt_item_details_id = models.AutoField(primary_key=True, validators=[MaxValueValidator(9999999999)])
    crt_item_color = models.CharField(max_length=7, null=False, blank=False)
    crt_item_size = models.CharField(max_length=3, choices=ITEM_SIZES, null=True, blank=True)
    crt_item_price = models.DecimalField(blank=False, null=False, decimal_places=2, max_digits=10, validators=[MinValueValidator(1.00)])  # *** set default price add minvalue
    crt_item_qty = models.PositiveIntegerField(validators=[MaxValueValidator(999)],blank=False, null=False)
    crt_item_SKU = models.CharField(max_length=16, null=False, blank=False, unique=True)
    crt_item_status = models.CharField(max_length=20, null=False, blank=False, choices=ITEM_STATUS, default="ACTIVE")  # *** set default as inactive but in ppt default is active
    crt_item = models.ForeignKey(tbl_creativeitems_mst, on_delete=models.CASCADE)

    def __str__(self):
        return self.crt_item_SKU


class tbl_crtimages(models.Model):
    crt_img_id = models.AutoField(primary_key=True, validators=[MaxValueValidator(99999)])
    crt_img_url = models.ImageField(max_length=150, null=True, upload_to='item-photos/', validators=[validate_image_file_extension])
    is_primary = models.BooleanField(default=False, null=False)
    crt_item_details = models.ForeignKey(tbl_creativeitems_details, on_delete=models.CASCADE)

    def __str__(self):
        return self.crt_item_details.crt_item.crt_item_name




# scrap items Model

class tbl_scrapitems(models.Model):
    scp_item_id = models.AutoField(primary_key=True, validators=[MaxValueValidator(9999999999)])
    scp_item_name = models.CharField(max_length=100, null=False, blank=False)
    scp_item_desc = models.TextField(blank=False, null=False)
    scp_item_price = models.DecimalField(blank=False, null=False, decimal_places=2, max_digits=10,
                                         validators=[MinValueValidator(1.00)])  # *** set default price add minvalue
    scp_item_qty = models.PositiveIntegerField(validators=[MaxValueValidator(999)], blank=False, null=False)
    scp_item_SKU = models.CharField(max_length=16, null=False, blank=False, unique=True)
    scp_item_status = models.CharField(max_length=20, null=False, blank=False, choices=ITEM_STATUS,
                                       default="ACTIVE")  # *** set default as inactive but in ppt default is active
    scp_created_on = models.DateTimeField(auto_now_add=True, null=False, blank=False)
    scp_last_modified = models.DateTimeField(auto_now_add=True, null=False, blank=False)
    scp_sub_category = models.ForeignKey(SubScrapCategory, on_delete=models.SET_DEFAULT,
                                         default=1)  # *** set default sub-category as other
    # user_id = models.ForeignKey( , on_delete=models.RESTRICT)
    # username = models.ForeignKey( , on_delete = models.RESTRICT)

    def __str__(self):
        return self.scp_item_name

class tbl_scrapimages(models.Model):
    scp_img_id = models.AutoField(primary_key=True, validators=[MaxValueValidator(99999)])
    scp_img_url = models.ImageField(max_length=150, null=True, upload_to='item-photos/', validators=[validate_image_file_extension])
    is_primary = models.BooleanField(default=False, null=False)
    scp_item = models.ForeignKey(tbl_scrapitems, on_delete=models.CASCADE)