from django.contrib import admin

from .models import License


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