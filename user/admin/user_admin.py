from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _


@admin.register(get_user_model())
class UserAdmin(BaseUserAdmin):
    ordering = ["-id"]

    list_display = ["email", "full_name"]

    search_fields = ["email", "full_name"]

    fieldsets = (
        (_("Data"), {"fields": ("email", "full_name", "password")}),
        ((_("Permissions")), {"fields": ("is_active", "is_superuser")}),
        (_("Important dates"), {"fields": ("last_login",)}),
    )

    add_fieldsets = (
        (None, {"classes": ("wide",), "fields": ("email", "password1", "password2"), },),
    )
