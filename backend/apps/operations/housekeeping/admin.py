from django.contrib import admin

from .models import HousekeepingTask


@admin.register(HousekeepingTask)
class HousekeepingTaskAdmin(admin.ModelAdmin):

    list_display = (
        "title",
        "room",
        "task_type",
        "priority",
        "status",
        "scheduled_date",
    )

    list_filter = (
        "task_type",
        "priority",
        "status",
        "scheduled_date",
    )

    search_fields = (
        "title",
        "room__room_number",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )