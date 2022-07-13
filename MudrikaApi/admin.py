from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(UserProfileSignUpData)
admin.site.register(AccessLevelTokenData)


class UserProfileDummyAdmin(admin.ModelAdmin):
    list_display = ("acc_address", "first_name", "last_name")
