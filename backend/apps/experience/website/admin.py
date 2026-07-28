from django.contrib import admin

from .models import Website


@admin.register(Website)
class WebsiteAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "tenant",
        "status",
        "is_active",
    )

    list_filter = (
        "status",
        "is_active",
    )

    search_fields = (
        "name",
        "title",
        "tenant__name",
    )

    autocomplete_fields = (
        "tenant",
    )