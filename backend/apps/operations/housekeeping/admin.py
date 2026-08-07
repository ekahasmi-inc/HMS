from django.contrib import admin

from .models import HousekeepingTask,HousekeepingAssignment


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



from .models import (
    HousekeepingTask,
    HousekeepingAssignment,
)


@admin.register(HousekeepingAssignment)
class HousekeepingAssignmentAdmin(admin.ModelAdmin):

    list_display = (
        "task",
        "assigned_to",
        "assignment_status",
        "planned_start",
        "actual_end",
    )

    list_filter = (
        "assignment_status",
    )

    search_fields = (
        "task__title",
        "assigned_to__username",
        "assigned_to__first_name",
        "assigned_to__last_name",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )