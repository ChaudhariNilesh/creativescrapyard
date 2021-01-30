from django.contrib import admin
from .models import tbl_crt_categories,tbl_crt_subcategories,MainScrapCategory,SubScrapCategory
# Register your models here.
admin.site.register(tbl_crt_categories)
admin.site.register(tbl_crt_subcategories)

admin.site.register(MainScrapCategory)
admin.site.register(SubScrapCategory)