from django.contrib import admin

from .models import Website, WebsiteTheme, WebsiteMenu, WebsiteMenuItem


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


@admin.register(WebsiteMenu)
class WebsiteMenuAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "website",
        "location",
        "is_active",
    )

    list_filter = (
        "location",
        "is_active",
    )

    search_fields = (
        "name",
        "slug",
        "website__name",
    )

    autocomplete_fields = (
        "website",
    )

@admin.register(WebsiteMenuItem)
class WebsiteMenuItemAdmin(admin.ModelAdmin):

    list_display = (
        "title",
        "menu",
        "parent",
        "display_order",
        "link_type",
        "is_visible",
    )

    list_filter = (
        "link_type",
        "is_visible",
    )

    search_fields = (
        "title",
        "slug",
        "url",
    )

    autocomplete_fields = (
        "menu",
        "parent",
    )

    ordering = (
        "menu",
        "display_order",
    )