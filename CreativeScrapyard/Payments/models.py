from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator,MinValueValidator
from Order.models import tbl_orders_mst

User = get_user_model()

PAYMENT_MODE = (
    ("PPI", "Paytm Wallet"),
    ("UPI", "UPI"),
    ("CC", "Credit Card"),
    ("DC", "Debit Card"),
    ("NB", "Net Banking"),
)

PAYMENT_STATUS = (
    (1, "Pending"),
    (2, "Success"),
    (3, "Failed"),
)


class Payment(models.Model):
    payment_id=models.AutoField(primary_key=True, validators=[MaxValueValidator(9999999999)])
    transaction_id = models.CharField(max_length=50,null=False,blank=False)
    payment_mode = models.CharField(max_length=3,choices=PAYMENT_MODE,null=False,blank=False)
    payment_date = models.DateTimeField(auto_now_add=True)
    payment_amt = models.DecimalField(blank=False, null=False, decimal_places=2, max_digits=15,
                                         validators=[MinValueValidator(1.00)])

    payment_status = models.PositiveIntegerField(choices=PAYMENT_STATUS)
    payment_remark = models.CharField(max_length=50, null=True, blank=True)
    order = models.ForeignKey(tbl_orders_mst,on_delete=models.DO_NOTHING)
    
    

    class Meta:
        db_table = 'tbl_payments'




class Transaction(models.Model):
    made_by = models.ForeignKey(User, related_name='transactions', 
                                on_delete=models.CASCADE)
    made_on = models.DateTimeField(auto_now_add=True)
    amount = models.IntegerField()
    order_id = models.CharField(unique=True, max_length=100, null=True, blank=True)
    checksum = models.CharField(max_length=100, null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.order_id is None and self.made_on and self.id:
            self.order_id = self.made_on.strftime('PAY2ME%Y%m%dODR') + str(self.id)
        return super().save(*args, **kwargs)


    