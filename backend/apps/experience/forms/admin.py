from django.contrib import admin

from .models import Form


@admin.register(Form)
class FormAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "website",
        "form_type",
        "status",
        "is_active",
    )

    list_filter = (
        "form_type",
        "status",
        "is_active",
    )

    search_fields = (
        "name",
        "title",
        "slug",
    )

    autocomplete_fields = (
        "tenant",
        "website",
    )

    prepopulated_fields = {
        "slug": ("name",)
    }