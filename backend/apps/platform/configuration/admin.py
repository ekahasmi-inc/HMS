from django.contrib import admin
from django.db import models
from django.forms import Textarea
from .models import (
    ConfigurationCategory,
    ConfigurationKey,
    ConfigurationValue,
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
    formfield_overrides = {
        models.JSONField: {
            "widget": Textarea(attrs={
                "rows": 6,
                "cols": 80,
            })
        }
    }

@admin.register(ConfigurationValue)
class ConfigurationValueAdmin(admin.ModelAdmin):

    list_display = (
        "tenant",
        "configuration_key",
        "value",
        "is_active",
    )

    list_filter = (
        "tenant",
        "is_active",
        "configuration_key__category",
    )

    search_fields = (
        "tenant__name",
        "configuration_key__name",
        "configuration_key__code",
        "value",
    )

    autocomplete_fields = (
        "tenant",
        "configuration_key",
    )