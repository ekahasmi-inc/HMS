from django.contrib import admin

from .models import Page


@admin.register(Page)
class PageAdmin(admin.ModelAdmin):

    list_display = (
        "title",
        "website",
        "status",
        "is_homepage",
        "display_order",
    )

    list_filter = (
        "status",
        "is_homepage",
    )

    search_fields = (
        "title",
        "slug",
        "path",
    )

    autocomplete_fields = (
        "website",
        "parent",
    )

    ordering = (
        "display_order",
        "title",
    )