from django.contrib import admin

from .models import SEOProfile, MetaTemplate, Redirect, SitemapConfig


@admin.register(SEOProfile)
class SEOProfileAdmin(admin.ModelAdmin):

    list_display = (
        "title",
        "robots_index",
        "robots_follow",
        "content_type",
        "created_at",
    )

    list_filter = (
        "robots_index",
        "robots_follow",
        "content_type",
    )

    search_fields = (
        "title",
        "meta_title",
        "meta_description",
    )

    ordering = (
        "title",
    )


@admin.register(MetaTemplate)
class MetaTemplateAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "template_type",
        "tenant",
        "is_default",
        "is_active",
    )

    list_filter = (
        "template_type",
        "is_default",
        "is_active",
    )

    search_fields = (
        "name",
        "title_template",
    )

    ordering = (
        "template_type",
        "name",
    )

@admin.register(Redirect)
class RedirectAdmin(admin.ModelAdmin):

    list_display = (
        "source_path",
        "destination_path",
        "redirect_type",
        "tenant",
        "is_active",
        "hit_count",
    )

    list_filter = (
        "redirect_type",
        "is_active",
    )

    search_fields = (
        "source_path",
        "destination_path",
    )

    ordering = (
        "source_path",
    )


@admin.register(SitemapConfig)
class SitemapConfigAdmin(admin.ModelAdmin):

    list_display = (
        "tenant",
        "enabled",
        "default_change_frequency",
        "default_priority",
        "auto_regenerate",
        "last_generated_at",
    )

    list_filter = (
        "enabled",
        "auto_regenerate",
        "ping_search_engines",
    )

    search_fields = (
        "tenant__name",
    )