from django.contrib import admin

from .models import OTAAccount, OTAProvider,OTAConnection


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


@admin.register(OTAAccount)
class OTAAccountAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "tenant",
        "provider",
        "account_reference",
        "account_email",
        "status",
        "connected_at",
        "last_synced_at",
        "created_at",
    )

    list_filter = (
        "status",
        "provider",
        "connected_at",
    )

    search_fields = (
        "name",
        "account_reference",
        "account_email",
        "account_username",
        "tenant__name",
        "provider__name",
    )

    autocomplete_fields = (
        "tenant",
        "provider",
    )

    ordering = (
        "tenant",
        "provider",
        "name",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    fieldsets = (
        (
            "Account Identity",
            {
                "fields": (
                    "tenant",
                    "provider",
                    "name",
                    "account_reference",
                )
            },
        ),
        (
            "Account Contact",
            {
                "fields": (
                    "account_email",
                    "account_username",
                )
            },
        ),
        (
            "Lifecycle",
            {
                "fields": (
                    "status",
                    "connected_at",
                    "last_synced_at",
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



@admin.register(OTAConnection)
class OTAConnectionAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "ota_account",
        "connection_type",
        "environment",
        "status",
        "sync_enabled",
        "last_connected_at",
    )

    list_filter = (
        "connection_type",
        "environment",
        "status",
        "sync_enabled",
    )

    search_fields = (
        "name",
        "ota_account__name",
        "ota_account__ota_provider__name",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    ordering = (
        "ota_account",
        "name",
    )