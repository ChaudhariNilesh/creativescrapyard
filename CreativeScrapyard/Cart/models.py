from Items.models import tbl_creativeitems_mst
from django.db import models
from Authentication.models import User
from django.core.validators import MaxValueValidator,MinValueValidator

# # Create your models here.

class Cart(models.Model):
    cart_id=models.AutoField(primary_key=True, validators=[MaxValueValidator(99999)])
    crt_item_qty=models.PositiveIntegerField(validators=[MinValueValidator(1)], default=1)
    crt_item=models.ForeignKey(tbl_creativeitems_mst,on_delete=models.CASCADE) #ITEM MODEL
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    
    class Meta:
        db_table = 'tbl_shoppingcart'

    def __str__(self):
        return self.user.username