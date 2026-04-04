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
        "get_role",
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
        "groups",
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

    def get_role(self, obj):
        group = obj.groups.first()
        return group.name if group else None
    get_role.short_description = "role"


admin.site.register(models.CustomUser, CustomUserAdmin)
