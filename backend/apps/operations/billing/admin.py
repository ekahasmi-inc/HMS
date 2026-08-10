from django.contrib import admin

from .models import Folio, FolioItem, Charge


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


@admin.register(FolioItem)
class FolioItemAdmin(admin.ModelAdmin):

    list_display = (
        "folio",
        "item_type",
        "description",
        "quantity",
        "unit_price",
        "amount",
        "currency",
        "service_date",
        "status",
        "source_type",
        "source_reference",
    )

    list_filter = (
        "item_type",
        "status",
        "currency",
        "service_date",
    )

    search_fields = (
        "folio__folio_number",
        "description",
        "source_type",
        "source_reference",
    )

    autocomplete_fields = (
        "tenant",
        "folio",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    ordering = (
        "service_date",
        "sort_order",
        "created_at",
    )


@admin.register(Charge)
class ChargeAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "code",
        "charge_type",
        "default_amount",
        "currency",
        "unit",
        "taxable",
        "active",
        "status",
        "sort_order",
    )

    list_filter = (
        "charge_type",
        "status",
        "active",
        "taxable",
        "currency",
    )

    search_fields = (
        "name",
        "slug",
        "code",
        "description",
    )

    autocomplete_fields = (
        "tenant",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    ordering = (
        "sort_order",
        "name",
    )