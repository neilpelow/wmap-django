from django.contrib import admin as admin_nongeo
from . import models
from django.contrib.auth import get_user_model
from django.contrib.gis import admin
from django.contrib.auth.admin import UserAdmin

# Register your models here.

class MyUserAdmin(UserAdmin):
    readonly_fields = ('id', 'last_login', 'date_joined', 'created', 'modified', )
    fieldsets = (
        (None, {'fields': ('id', 'username', 'email', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name')}),
        ('Account Status', {'fields': ('is_active', 'is_staff', 'is_superuser', )}),
        ('Dates', {'fields': ('last_login', 'date_joined', 'created', 'modified')}),
        ('Location', {'fields': ('last_location',)}),
    )

admin.site.register(get_user_model(), MyUserAdmin)
admin.site.register(models.FriendGroup, admin.OSMGeoAdmin)
admin.site.register(models.UserFriendGroup, admin.OSMGeoAdmin)
