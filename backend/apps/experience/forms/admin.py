from django.contrib import admin
from .models import (
    Form,
    FormField,
    FormSubmission,
)


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


@admin.register(FormField)
class FormFieldAdmin(admin.ModelAdmin):

    list_display = (
        "label",
        "form",
        "field_type",
        "display_order",
        "is_required",
        "is_active",
    )

    list_filter = (
        "field_type",
        "is_required",
        "is_active",
    )

    search_fields = (
        "label",
        "name",
        "slug",
    )

    autocomplete_fields = (
        "form",
    )

    ordering = (
        "form",
        "display_order",
    )

    prepopulated_fields = {
        "slug": ("label",)
    }

@admin.register(FormSubmission)
class FormSubmissionAdmin(admin.ModelAdmin):

    list_display = (
        "form",
        "submitter_name",
        "submitter_email",
        "status",
        "submitted_at",
        "is_spam",
    )

    list_filter = (
        "status",
        "is_spam",
        "submitted_at",
    )

    search_fields = (
        "submitter_name",
        "submitter_email",
        "submitter_phone",
    )

    autocomplete_fields = (
        "tenant",
        "form",
        "submitted_by",
    )

    readonly_fields = (
        "submitted_at",
    )

    ordering = (
        "-submitted_at",
    )