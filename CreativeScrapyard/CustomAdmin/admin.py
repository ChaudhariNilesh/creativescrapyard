from django.contrib import admin
from .models import tbl_crt_categories,tbl_crt_subcategories,MainScrapCategory,SubScrapCategory,Badges,BadgeEntries
# Register your models here.
admin.site.register(tbl_crt_categories)
admin.site.register(tbl_crt_subcategories)

admin.site.register(MainScrapCategory)
admin.site.register(SubScrapCategory)
admin.site.register(Badges)
admin.site.register(BadgeEntries)