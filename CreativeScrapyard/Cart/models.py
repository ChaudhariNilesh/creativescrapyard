# from django.db import models
# from django.contrib.auth.models import AbstractUser
# # Create your models here.

# class Cart(models.Model):
#     cart_id=models.AutoField(primary_key=True, validators=[MaxValueValidator(99999)])
#     crt_item_qty=models.PositiveIntegerField(validators=[MinValueValidator(1)], default=1)
#     crt_item_details_id=models.ForeignKey(tbl_creativeitems_details,on_delete=models.CASCADE) #ITEM MODEL
#     user=models.ForeignKey(User,on_delete=models.CASCADE)
    
#     class Meta:
#         db_table = 'tbl_shoppingcart'

#     def __str__(self):
#         return self.user.username