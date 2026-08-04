from django.contrib import admin

from .models import InventoryCalendar


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