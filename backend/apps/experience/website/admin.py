from django.contrib import admin

from .models import Website, WebsiteTheme


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

@admin.register(WebsiteTheme)
class WebsiteThemeAdmin(admin.ModelAdmin):

    list_display = (
        "website",
        "theme_name",
        "theme_slug",
        "mode",
        "version",
        "is_active",
    )

    list_filter = (
        "mode",
        "is_active",
    )

    search_fields = (
        "website__name",
        "theme_name",
        "theme_slug",
    )

    autocomplete_fields = (
        "website",
    )