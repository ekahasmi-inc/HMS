from django.contrib import admin

from .models import (
    HousekeepingTask,
    HousekeepingAssignment,
    HousekeepingStatusLog,
    MaintenanceRequest,
    MaintenanceLog,
    CleaningChecklist,
)


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


@admin.register(HousekeepingStatusLog)
class HousekeepingStatusLogAdmin(admin.ModelAdmin):

    list_display = (
        "assignment",
        "previous_status",
        "new_status",
        "change_source",
        "changed_by",
        "created_at",
    )

    list_filter = (
        "new_status",
        "change_source",
    )

    search_fields = (
        "assignment__task__title",
        "remarks",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )



@admin.register(MaintenanceRequest)
class MaintenanceRequestAdmin(admin.ModelAdmin):

    list_display = (
        "title",
        "property",
        "room",
        "category",
        "priority",
        "status",
        "scheduled_date",
    )

    list_filter = (
        "category",
        "priority",
        "status",
    )

    search_fields = (
        "title",
        "room__room_number",
        "description",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )


@admin.register(MaintenanceLog)
class MaintenanceLogAdmin(admin.ModelAdmin):

    list_display = (
        "request",
        "technician",
        "work_status",
        "labor_hours",
        "total_cost",
        "created_at",
    )

    list_filter = (
        "work_status",
    )

    search_fields = (
        "request__title",
        "technician__username",
        "work_performed",
    )

    readonly_fields = (
        "total_cost",
        "created_at",
        "updated_at",
    )




@admin.register(CleaningChecklist)
class CleaningChecklistAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "property",
        "checklist_type",
        "version",
        "status",
        "is_default",
    )


    list_filter = (
        "checklist_type",
        "status",
    )


    search_fields = (
        "name",
        "description",
    )


    readonly_fields = (
        "created_at",
        "updated_at",
    )