from django.contrib import admin

from .models import License, LicenseKey


@admin.register(License)
class LicenseAdmin(admin.ModelAdmin):

    list_display = (
        "tenant",
        "license_type",
        "status",
        "valid_from",
        "valid_until",
    )

    list_filter = (
        "license_type",
        "status",
    )

    search_fields = (
        "tenant__name",
    )

    autocomplete_fields = (
        "tenant",
        "subscription",
    )

@admin.register(LicenseKey)
class LicenseKeyAdmin(admin.ModelAdmin):

    list_display = (
        "license",
        "key",
        "status",
        "issued_at",
        "expires_at",
    )

    list_filter = (
        "status",
    )

    search_fields = (
        "key",
        "license__tenant__name",
    )

    autocomplete_fields = (
        "license",
    )