from django.db import models
from django.core.validators import MaxValueValidator,MinValueValidator


# Create your models here.

class tbl_creativeitems_mst(models.Model):
    crt_item_id = models.PositiveIntegerField(primary_key=True, validators=[MaxValueValidator(9999999999)])
    crt_item_name = models.CharField(max_length=100, null=False, blank=False)
    crt_item_desc = models.TextField(blank=True, null=True)
    crt_created_on = models.DateTimeField(auto_now_add=True, null=False, blank=False)
    crt_last_modified = models.DateTimeField(auto_now_add=True, null=False, blank=False)
    # crt_sub_category = models.ForeignKey( ,on_delete=models.SET_DEFAULT, default=)   # *** set default sub-category as other
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


WEIGHT_CHOICES = (
    ("Below 100g", "Below 100g"),
    ("Below 250g", "Below 250g"),
    ("Below 500g", "Below 500g"),
    ("Below 1kg", "Below 1kg"),
    ("Below 5kg", "Below 5kg"),
)

ITEM_STATUS = (
    ("INAPPROPRIATE","Inappropriate"),
    ("ACTIVE","Active"),
    ("INACTIVE","Inactive"),
    ("SOLD","Sold",)
)

class tbl_creativeitems_details(models.Model):
    crt_item_details_id = models.PositiveIntegerField(primary_key=True, validators=[MaxValueValidator(9999999999)])
    crt_item_color = models.CharField(max_length=7)
    crt_item_size = models.CharField(max_length=3, choices=ITEM_SIZES, null=True, blank=True)
    crt_item_price = models.DecimalField(blank=False, null=False, decimal_places=2, max_digits=10, validators=[MinValueValidator(0)])  # *** set default price add minvalue
    crt_item_qty = models.PositiveIntegerField(validators=[MaxValueValidator(999)],blank=False, null=False)
    crt_item_weight = models.CharField(max_length=10, choices=WEIGHT_CHOICES,blank=True, null=True)
    crt_item_height = models.DecimalField(decimal_places=2, max_digits=5)
    crt_item_width = models.DecimalField(decimal_places=2, max_digits=5)
    crt_item_SKU = models.CharField(max_length=16, null=False, blank=False)
    crt_item_status = models.CharField(max_length=20, null=False, blank=False, choices=ITEM_STATUS, default="INACTIVE")  # *** set default as inactive but in ppt default is active
    crt_item = models.ForeignKey(tbl_creativeitems_mst, on_delete=models.CASCADE)

    def __str__(self):
        return self.crt_item_details_id


class tbl_crtimages(models.Model):
    crt_img_id = models.PositiveIntegerField(primary_key=True, validators=[MaxValueValidator(99999)])
    crt_img_url = models.ImageField(max_length=150, null=True, upload_to='photos/')
    is_primary = models.BooleanField(default=False, null=False)
    crt_item_details = models.ForeignKey(tbl_creativeitems_details, on_delete=models.CASCADE)

    def __str__(self):
        return self.crt_img_id