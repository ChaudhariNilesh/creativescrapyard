from django.contrib import admin
# from django.contrib.auth.admin import UserAdmin
from .models import *

# Register your models here.
# admin.site.register(Photo)

# class UserAdmin(UserAdmin):
#     model = User
#     list_display = ['user_id', 'username', 'first_name', 'last_name', 'email', 'password', 'is_active']

admin.site.register(User)
admin.site.register(Profile)
admin.site.register(Address)
admin.site.register(Cities)
admin.site.register(States)
admin.site.register(Documents)



