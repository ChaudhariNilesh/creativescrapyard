from django.db import models
from django.core.validators import MaxValueValidator,MinValueValidator
from Items.models import tbl_creativeitems_details

# Create your models here.

DELIVERY_STATUS = (
    ("PENDING", "Pending"),
    ("DISPATCHED", "Dispatched"),
    ("DELIVERED", "Delivered"),
    ("CANCELLED", "Cancelled",)
)

class tbl_orders_mst(models.Model):
    order_id = models.PositiveIntegerField(primary_key=True, validators=[MaxValueValidator(9999999999)])
    person_name = models.CharField(max_length=20, null=False, blank=False)
    contact_no = models.CharField(max_length=10, null=False, blank=False)   # set fixed length 10 on forms
    delivery_address = models.CharField(max_length=350, null=False, blank=False)
    total_amt = models.DecimalField(max_digits=15, decimal_places=2, null=False, blank=False, validators=[MinValueValidator(0)])
    order_date = models.DateTimeField(auto_now_add=True, null=False, blank=False)
    delivery_status = models.CharField(max_length=15, null=False, blank=False, choices=DELIVERY_STATUS)   # *** review choice field
    delivery_date = models.DateTimeField(auto_now_add=True, null=False)
    # user_id = models.ForeignKey( , on_delete = models.RESTRICT)       # *** reference user model

    def __str__(self):
        return self.order_id


ITEM_STATUS = (
    ("PLACED","Placed"),
    ("COMPLETED", "Completed"),
    ("CANCELLED", "Cancelled"),
    ("FAILED", "Failed"),
    ("RETURNED", "Returned"),
)

class tbl_orders_details(models.Model):
    order_details_id = models.PositiveIntegerField(primary_key=True, validators=[MaxValueValidator(9999999999)])
    crt_item_qty = models.PositiveIntegerField(validators=[MaxValueValidator(999)], default=1, null=False, blank=False)
    unit_price = models.DecimalField(max_digits=15, decimal_places=2, null=False, blank=False, validators=[MinValueValidator(0)])
    pickup_address = models.CharField(max_length=350, null=False, blank=False)            # *** it should be Charfield or reference from address table?
    item_status = models.CharField(max_length=15, null=False, blank=False, choices=ITEM_STATUS)          # *** Review choice field
    order = models.ForeignKey(tbl_orders_mst, on_delete=models.RESTRICT)
    crt_item_details = models.ForeignKey(tbl_creativeitems_details, on_delete=models.RESTRICT, null=True)  # *** review on_delete

    def __str__(self):
        return self.order_details_id