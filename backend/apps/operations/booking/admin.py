from django.contrib import admin
from .models import (
    Property,
    PropertyAmenity,
)

@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "tenant",
        "property_type",
        "status",
        "city",
        "country",
    )

    list_filter = (
        "property_type",
        "status",
        "country",
    )

    search_fields = (
        "name",
        "city",
        "state",
    )

    prepopulated_fields = {
        "slug": ("name",),
    }

    autocomplete_fields = (
        "tenant",
    )

@admin.register(PropertyAmenity)
class PropertyAmenityAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "property",
        "category",
        "is_featured",
        "is_active",
        "display_order",
    )

    list_filter = (
        "category",
        "is_active",
        "is_featured",
    )

    search_fields = (
        "name",
        "property__name",
    )

    autocomplete_fields = (
        "property",
    )

    prepopulated_fields = {
        "slug": ("name",),
    }

    ordering = (
        "property",
        "display_order",
        "name",
    )