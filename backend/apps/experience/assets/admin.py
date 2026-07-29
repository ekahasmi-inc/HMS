from django.contrib import admin

from .models import MediaFolder


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