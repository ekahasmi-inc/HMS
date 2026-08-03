from django.contrib import admin

from .models import Property


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
