from django.contrib import admin

from .models import Folio, FolioItem, Charge, TaxLine, Discount


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





@admin.register(TaxLine)
class TaxLineAdmin(admin.ModelAdmin):

    list_display = (
        "folio_item",
        "tax_type",
        "tax_name",
        "tax_rate",
        "taxable_amount",
        "tax_amount",
        "currency",
    )

    list_filter = (
        "tax_type",
        "currency",
    )

    search_fields = (
        "tax_name",
        "folio_item__description",
    )

    autocomplete_fields = (
        "folio_item",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    ordering = (
        "tax_type",
        "tax_name",
    )



@admin.register(Discount)
class DiscountAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "folio_item",
        "discount_type",
        "base_amount",
        "discount_rate",
        "discount_amount",
        "currency",
        "source_type",
    )

    list_filter = (
        "discount_type",
        "currency",
        "source_type",
    )

    search_fields = (
        "name",
        "description",
        "source_reference",
        "folio_item__description",
        "folio_item__folio__folio_number",
    )

    ordering = (
        "folio_item",
        "id",
    )