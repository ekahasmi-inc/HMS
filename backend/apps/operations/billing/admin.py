from django.contrib import admin

from .models import Folio


@admin.register(Folio)
class FolioAdmin(admin.ModelAdmin):

    list_display = (
        "folio_number",
        "folio_type",
        "reservation",
        "guest",
        "property",
        "status",
        "currency",
        "opening_balance",
        "closing_balance",
        "opened_at",
        "closed_at",
    )

    list_filter = (
        "folio_type",
        "status",
        "currency",
        "property",
    )

    search_fields = (
        "folio_number",
        "reservation__booking_number",
        "guest_name",
    )

    autocomplete_fields = (
        "tenant",
        "property",
        "reservation",
        "guest",
        "closed_by",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    ordering = (
        "-created_at",
    )