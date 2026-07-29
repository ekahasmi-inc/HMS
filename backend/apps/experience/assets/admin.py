from django.contrib import admin

from .models import MediaFolder, MediaAsset


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