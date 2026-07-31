from django.contrib import admin

from .models import SEOProfile


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