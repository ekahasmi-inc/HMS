from django.contrib import admin

from .models import ConfigurationCategory


@admin.register(ConfigurationCategory)
class ConfigurationCategoryAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "code",
        "display_order",
        "is_active",
    )

    list_filter = (
        "is_active",
    )

    search_fields = (
        "name",
        "code",
    )

    ordering = (
        "display_order",
        "name",
    )

    prepopulated_fields = {
        "code": ("name",)
    }