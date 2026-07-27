from django.contrib import admin

from .models import Tenant,TenantDomain


@admin.register(Tenant)
class TenantAdmin(admin.ModelAdmin):
    list_display = ("name","slug", "email", "is_active", "created_at",)

    search_fields = ( "name", "email",)

    list_filter = ("is_active",)

    prepopulated_fields = {
        "slug": ("name",)
    }

@admin.register(TenantDomain)
class TenantDomainAdmin(admin.ModelAdmin):
    list_display = ("domain", "tenant", "is_primary", "is_verified", "ssl_enabled",  "status",)

    list_filter = ("status","is_primary","is_verified","ssl_enabled",)

    search_fields = ("domain", "tenant__name",)