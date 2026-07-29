from django.contrib import admin

from .models import MediaFolder, MediaAsset, MediaVariant


@admin.register(MediaFolder)
class MediaFolderAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "tenant",
        "parent",
        "display_order",
        "is_system",
        "is_active",
    )

    list_filter = (
        "tenant",
        "is_system",
        "is_active",
    )

    search_fields = (
        "name",
        "slug",
    )

    ordering = (
        "tenant",
        "display_order",
        "name",
    )

@admin.register(MediaAsset)
class MediaAssetAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "asset_type",
        "storage_provider",
        "source_type",
        "tenant",
        "is_active",
    )

    list_filter = (
        "asset_type",
        "storage_provider",
        "source_type",
        "tenant",
    )

    search_fields = (
        "name",
        "title",
        "provider_asset_id",
    )

@admin.register(MediaVariant)
class MediaVariantAdmin(admin.ModelAdmin):

    list_display = (
        "asset",
        "variant_type",
        "width",
        "height",
        "mime_type",
        "processing_status",
        "created_at",
    )

    list_filter = (
        "variant_type",
        "processing_status",
        "mime_type",
    )

    search_fields = (
        "asset__name",
        "asset__title",
    )
