from django.db import models
from django.core.validators import MaxValueValidator,MinValueValidator
from Items.models import tbl_creativeitems_mst
from django.contrib.auth.models import AbstractUser
from Authentication.models import User
from datetime import datetime,timedelta
from django.utils import timezone
# Create your models here.

DELIVERY_STATUS = (
    (1, "Pending"),
    (2, "Dispatched"),
    (3, "Delivered"),
    (4, "Cancelled",)
)

ITEM_STATUS = (
    (1, "Pending"),
    (2, "Completed"),
    (3, "Cancelled"),
    (4, "Failed"),
    (5, "Returned"),
)
# ORDER_STATUS = (
#     (1, "Pending"),
#     (2, "Success"),
#     (3, "Failed"),
# )

def getDeliveryDate():
    return timezone.now()+timedelta(days=6)

class tbl_orders_mst(models.Model):
    order_id = models.AutoField(primary_key=True, validators=[MaxValueValidator(9999999999)])
    person_name = models.CharField(max_length=20, null=False, blank=False)
    contact_no = models.CharField(max_length=10, null=False, blank=False)   
    delivery_address = models.TextField(max_length=350, null=False, blank=False)
    total_amt = models.DecimalField(max_digits=15, decimal_places=2, null=False, blank=False, validators=[MinValueValidator(1.00)])
    order_date = models.DateTimeField(auto_now_add=True, null=False, blank=False)
    order_status = models.BooleanField(null=False, blank=False,default=False)   
    delivery_status = models.PositiveIntegerField(null=False, blank=False, choices=DELIVERY_STATUS)   
    delivery_date = models.DateTimeField(default=getDeliveryDate,null=False)
    user= models.ForeignKey(User, on_delete = models.RESTRICT)       

    def __str__(self):
        return self.person_name
   




class tbl_orders_details(models.Model):
    order_details_id = models.AutoField(primary_key=True, validators=[MaxValueValidator(9999999999)])
    crt_item_qty = models.PositiveIntegerField(validators=[MaxValueValidator(999)], default=1, null=False, blank=False)
    unit_price = models.DecimalField(max_digits=15, decimal_places=2, null=False, blank=False, validators=[MinValueValidator(1.0)])
    pickup_address = models.CharField(max_length=350, null=False, blank=False)            
    item_status = models.PositiveIntegerField(null=False, blank=False, choices=ITEM_STATUS)    
    order = models.ForeignKey(tbl_orders_mst, on_delete=models.CASCADE)
    crt_item_mst = models.ForeignKey(tbl_creativeitems_mst, on_delete=models.RESTRICT, null=True)  

    def __str__(self):
        return self.order.person_name
