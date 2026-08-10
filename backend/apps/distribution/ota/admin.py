from django.contrib import admin

from .models import OTAProvider


@admin.register(OTAProvider)
class OTAProviderAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "code",
        "provider_type",
        "status",
        "api_supported",
        "webhook_supported",
        "reservation_sync_supported",
        "availability_sync_supported",
        "rate_sync_supported",
        "sort_order",
        "created_at",
    )

    list_filter = (
        "provider_type",
        "status",
        "api_supported",
        "webhook_supported",
        "reservation_sync_supported",
        "availability_sync_supported",
        "rate_sync_supported",
    )

    search_fields = (
        "name",
        "code",
        "display_name",
        "description",
    )

    ordering = (
        "sort_order",
        "name",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    fieldsets = (
        (
            "Provider Identity",
            {
                "fields": (
                    "code",
                    "name",
                    "display_name",
                    "provider_type",
                    "description",
                    "website_url",
                )
            },
        ),
        (
            "Capabilities",
            {
                "fields": (
                    "api_supported",
                    "webhook_supported",
                    "reservation_sync_supported",
                    "availability_sync_supported",
                    "rate_sync_supported",
                )
            },
        ),
        (
            "Lifecycle",
            {
                "fields": (
                    "status",
                    "sort_order",
                )
            },
        ),
        (
            "Metadata",
            {
                "fields": (
                    "metadata",
                )
            },
        ),
        (
            "Audit",
            {
                "fields": (
                    "created_at",
                    "updated_at",
                )
            },
        ),
    )