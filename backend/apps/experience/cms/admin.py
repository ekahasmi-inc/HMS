from django.contrib import admin

from .models import Page, PageRevision, ContentBlock, Component


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


@admin.register(ContentBlock)
class ContentBlockAdmin(admin.ModelAdmin):

    list_display = (
        "identifier",
        "page",
        "block_type",
        "display_order",
        "is_visible",
    )

    list_filter = (
        "block_type",
        "is_visible",
    )

    search_fields = (
        "identifier",
        "title",
        "page__title",
    )

    autocomplete_fields = (
        "page",
    )

    ordering = (
        "page",
        "display_order",
    )


@admin.register(Component)
class ComponentAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "code",
        "category",
        "version",
        "is_system",
        "is_active",
    )

    list_filter = (
        "category",
        "is_system",
        "is_active",
    )

    search_fields = (
        "name",
        "code",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )