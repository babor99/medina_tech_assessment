from django.contrib import admin
from django.contrib.auth.models import Group

from .models import *


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
	list_display = [field.name for field in User._meta.fields]


@admin.register(Vendor)
class VendorAdmin(admin.ModelAdmin):
	list_display = [field.name for field in Vendor._meta.fields]


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
	list_display = [field.name for field in Customer._meta.fields]


admin.site.unregister(Group)
