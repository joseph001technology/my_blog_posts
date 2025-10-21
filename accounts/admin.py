from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import UserAccount, Profile

 
 

class CustomUserAdmin(UserAdmin):
    model = UserAccount
    list_display = ("email", "user_name", "first_name", "is_staff", "is_active")
    list_filter = ("is_staff", "is_active", "groups")
    ordering = ("email",)

    fieldsets = (
        (None, {"fields": ("email", "user_name", "first_name", "password")}),
        ("Permissions", {"fields": ("is_staff", "is_active", "groups", "user_permissions")}),
        ("Important dates", {"fields": ("last_login",)}),
    )

    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("email", "user_name", "first_name", "password1", "password2", "is_staff", "is_active", "groups", "user_permissions"),
        }),
    )

    search_fields = ("email", "user_name")

admin.site.register(UserAccount, CustomUserAdmin)
admin.site.register(Profile)
