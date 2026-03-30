from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from . import models

# Register your models here.


class CustomUserAdmin(UserAdmin):
    model = models.CustomUser
    list_display = (
        "email",
        "first_name",
        "last_name",
        "phone",
        "identification_number",
        "business_id",
        "role",
        "is_staff",
        "is_active",
    )
    list_filter = (
        "email",
        "first_name",
        "last_name",
        "phone",
        "identification_number",
        "business_id",
        "role",
        "is_staff",
        "is_active",
    )
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "first_name",
                    "last_name",
                    "email",
                    "password",
                    "phone",
                    "identification_number",
                    "business_id",
                    "role",
                )
            },
        ),
        (
            "Permissions",
            {"fields": ("is_staff", "is_active", "groups", "user_permissions")},
        ),
    )
    add_fieldsets = (
        (
            None,
            {
                "fields": (
                    "first_name",
                    "last_name",
                    "email",
                    "password1",
                    "password2",
                    "phone",
                    "identification_number",
                    "business_id",
                    "role",
                    "is_staff",
                    "is_active",
                    "groups",
                    "user_permissions",
                )
            },
        ),
    )
    search_fields = ("email",)
    ordering = ("email",)


admin.site.register(models.CustomUser, CustomUserAdmin)
