from django.contrib import admin
from .models import (
    InventoryCalendar,
    InventoryBlock,
    InventoryAdjustment,
    AvailabilityRule
)

@admin.register(InventoryCalendar)
class InventoryCalendarAdmin(admin.ModelAdmin):

    list_display = (
        "room",
        "date",
        "status",
        "is_available",
        "available_count",
    )

    list_filter = (
        "status",
        "is_available",
        "date",
    )

    search_fields = (
        "room__room_number",
    )

    ordering = (
        "date",
        "room",
    )

    date_hierarchy = "date"


@admin.register(InventoryBlock)
class InventoryBlockAdmin(admin.ModelAdmin):

    list_display = (
        "title",
        "room",
        "block_type",
        "start_date",
        "end_date",
        "status",
    )

    list_filter = (
        "block_type",
        "status",
    )

    search_fields = (
        "title",
        "room__room_number",
    )

    ordering = (
        "-start_date",
    )


@admin.register(InventoryAdjustment)
class InventoryAdjustmentAdmin(admin.ModelAdmin):

    list_display = (
        "inventory",
        "adjustment_type",
        "previous_status",
        "new_status",
        "adjusted_by",
        "created_at",
    )

    list_filter = (
        "adjustment_type",
    )

    search_fields = (
        "inventory__room__room_number",
        "reason",
        "reference_id",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    ordering = (
        "-created_at",
    )

@admin.register(AvailabilityRule)
class AvailabilityRuleAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "property",
        "rule_type",
        "minimum_stay",
        "maximum_stay",
        "status",
    )

    list_filter = (
        "rule_type",
        "status",
    )

    search_fields = (
        "name",
        "property__name",
    )

    ordering = (
        "property",
        "name",
    )