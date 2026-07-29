from django.contrib import admin

from .models import Page, PageRevision


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

@admin.register(PageRevision)
class PageRevisionAdmin(admin.ModelAdmin):

    list_display = (
        "page",
        "version",
        "status",
        "created_by",
        "published_at",
    )

    list_filter = (
        "status",
    )

    search_fields = (
        "page__title",
        "title",
    )

    autocomplete_fields = (
        "page",
        "created_by",
        "published_by",
    )

    ordering = (
        "-version",
    )