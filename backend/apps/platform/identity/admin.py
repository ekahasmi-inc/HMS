from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Role, User, Permission, RolePermission


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    model = User

@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):

    list_display = ("name", "code", "is_system_role", "is_active",)
    list_filter = ("is_system_role", "is_active",)
    search_fields = ("name", "code",)

@admin.register(Permission)
class PermissionAdmin(admin.ModelAdmin):

    list_display = ("code", "module", "scope", "is_active",)
    list_filter = (
        "module",
        "scope",
        "is_active",
    )

    search_fields = (
        "code",
        "name",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )

@admin.register(RolePermission)
class RolePermissionAdmin(admin.ModelAdmin):

    list_display = (
        "role",
        "permission",
        "is_granted",
    )

    list_filter = (
        "role",
        "permission__module",
        "is_granted",
    )

    search_fields = (
        "role__name",
        "permission__code",
    )

    autocomplete_fields = (
        "role",
        "permission",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )
    