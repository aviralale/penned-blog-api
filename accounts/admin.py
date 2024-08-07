from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group
from .models import User


class UserAdmin(BaseUserAdmin):
    # The fields to be used in displaying the User model.
    list_display = ("username", "display_name", "is_admin", "is_active")
    list_filter = ("is_admin", "is_active")

    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (
            "Personal info",
            {
                "fields": (
                    "display_name",
                    "username",
                    "profile_pic",
                    "bio",
                    "gender",
                    "date_of_birth",
                )
            },
        ),
        (
            "Permissions",
            {
                "fields": (
                    "is_admin",
                    "is_active",
                    "is_staff",
                    "is_superuser",
                )
            },
        ),
        ("Important dates", {"fields": ("last_login",)}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "display_name",
                    "username",
                    "password1",
                    "password2",
                    "is_admin",
                ),
            },
        ),
    )
    search_fields = ("email", "display_name", "username")
    ordering = ("email",)
    filter_horizontal = ()


admin.site.register(User, UserAdmin)
admin.site.unregister(Group)
