from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from users.models import User


@admin.register(User)
class UserAdmin(UserAdmin):
    model = User
    list_display = ('username', 'email', "role", 'is_staff',"is_staff", "is_active", "is_verified" )
    list_filter = ("role", "is_staff", "is_active", "is_verified")
    fieldsets = (
        (None, {'fields': ("email",'username', 'password',"phone", "country","role", "is_verified")}),
        ("Permissions", {'fields': ("is_staff", "is_active", "is_superuser","groups", "user_permissions")}),
    )
    add_fieldsets = (
        (None, {"fields": ("email", "username", "password1", "password2", "phone","role", "is_verified", "is_staff","is_active")}),
    )
    search_fields = ("email", "username", "phone")
    ordering = ("email",)
