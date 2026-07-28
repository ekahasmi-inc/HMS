from django.contrib import admin
from .models import (
    ConfigurationCategory,
    ConfigurationKey,
)


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

@admin.register(ConfigurationKey)
class ConfigurationKeyAdmin(admin.ModelAdmin):

    list_display = ("name", "category", "data_type", "is_required", "is_system", "is_active",)
    list_filter = ("category", "data_type", "is_active",)
    search_fields = ("name", "code", "description",)
    autocomplete_fields = ("category",)
    ordering = ("category", "display_order", "name",)
    prepopulated_fields = {
        "code": ("name",)
    }