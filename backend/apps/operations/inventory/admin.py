from django.contrib import admin

from .models import InventoryCalendar, InventoryBlock


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