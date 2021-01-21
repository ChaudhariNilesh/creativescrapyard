from django.contrib import admin
from .models import MainCreativeCategory,SubCreativeCategory,MainScrapCategory,SubScrapCategory
# Register your models here.
admin.site.register(MainCreativeCategory)
admin.site.register(SubCreativeCategory)

admin.site.register(MainScrapCategory)
admin.site.register(SubScrapCategory)