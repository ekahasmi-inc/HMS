from django.db import models
from django.conf import settings
from apps.operations.booking.models import Property, Room
from apps.platform.common.models import TimeStampedModel
from datetime import timedelta
from django.utils import timezone


class HousekeepingTask(TimeStampedModel):
    """
    Defines a housekeeping task for a room.
    """

    class TaskType(models.TextChoices):
        CHECKOUT_CLEANING = "checkout_cleaning", "Checkout Cleaning"
        STAYOVER_CLEANING = "stayover_cleaning", "Stay-over Cleaning"
        DEEP_CLEANING = "deep_cleaning", "Deep Cleaning"
        INSPECTION = "inspection", "Inspection"
        LINEN_CHANGE = "linen_change", "Linen Change"
        TURNDOWN = "turndown", "Turndown Service"
        SANITIZATION = "sanitization", "Sanitization"
        EMERGENCY = "emergency", "Emergency Cleaning"

    class Priority(models.TextChoices):
        LOW = "low", "Low"
        NORMAL = "normal", "Normal"
        HIGH = "high", "High"
        URGENT = "urgent", "Urgent"


    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        IN_PROGRESS = "in_progress", "In Progress"
        COMPLETED = "completed", "Completed"
        CANCELLED = "cancelled", "Cancelled"


    property = models.ForeignKey(
        Property,
        on_delete=models.CASCADE,
        related_name="housekeeping_tasks",
    )


    room = models.ForeignKey(
        Room,
        on_delete=models.CASCADE,
        related_name="housekeeping_tasks",
    )


    title = models.CharField(
        max_length=200,
    )


    task_type = models.CharField(
        max_length=40,
        choices=TaskType.choices,
    )


    priority = models.CharField(
        max_length=20,
        choices=Priority.choices,
        default=Priority.NORMAL,
    )


    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING,
    )


    scheduled_date = models.DateField()


    estimated_duration_minutes = models.PositiveIntegerField(
        default=30,
    )


    instructions = models.TextField(
        blank=True,
    )


    metadata = models.JSONField(
        default=dict,
        blank=True,
    )


    class Meta:

        ordering = [
            "scheduled_date",
            "priority",
        ]


        constraints = [

            models.UniqueConstraint(
                fields=[
                    "room",
                    "scheduled_date",
                    "task_type",
                ],
                name="uq_housekeeping_room_task_date",
            ),

        ]


        indexes = [

            models.Index(
                fields=[
                    "property",
                    "scheduled_date",
                ],
                name="idx_hk_property_date",
            ),

            models.Index(
                fields=[
                    "room",
                    "status",
                ],
                name="idx_hk_room_status",
            ),

            models.Index(
                fields=[
                    "priority",
                    "status",
                ],
                name="idx_hk_priority_status",
            ),

        ]


    def __str__(self):

        return f"{self.room.room_number} - {self.title}"


class HousekeepingAssignment(TimeStampedModel):
    """
    Assignment of a housekeeping task to a staff member.
    """
    class Status(models.TextChoices):
        ASSIGNED = "assigned", "Assigned"
        ACCEPTED = "accepted", "Accepted"
        IN_PROGRESS = "in_progress", "In Progress"
        COMPLETED = "completed", "Completed"
        CANCELLED = "cancelled", "Cancelled"
        REASSIGNED = "reassigned", "Reassigned"

    task = models.ForeignKey(HousekeepingTask, on_delete=models.CASCADE, related_name="assignments",)
    assigned_to = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name="housekeeping_assignments",)
    assigned_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name="housekeeping_assignments_created",)
    assignment_status = models.CharField(max_length=20, choices=Status.choices, default=Status.ASSIGNED,)
    planned_start = models.DateTimeField(null=True, blank=True,)
    planned_end = models.DateTimeField(null=True, blank=True,)
    actual_start = models.DateTimeField(null=True, blank=True,)
    actual_end = models.DateTimeField(null=True, blank=True,)
    completion_percentage = models.PositiveSmallIntegerField(default=0,)
    notes = models.TextField(blank=True,)
    metadata = models.JSONField(default=dict, blank=True,)

    class Meta:

        ordering = [
            "-created_at",
        ]


        constraints = [

            models.UniqueConstraint(
                fields=[
                    "task",
                    "assigned_to",
                ],
                name="uq_housekeeping_task_assign",
            ),
        ]

        indexes = [
            models.Index(
                fields=["assigned_to", "assignment_status",],
                name="idx_hk_assign_user_status",
            ),
            models.Index(
                fields=["task", "assignment_status",],
                name="idx_hk_assign_task_status",
            ),
        ]

    def __str__(self):

        return (
            f"{self.task.title} → "
            f"{self.assigned_to or 'Unassigned'}"
        )



from django.conf import settings


class HousekeepingStatusLog(TimeStampedModel):
    """
    Immutable audit log for housekeeping assignment status changes.
    """

    class Status(models.TextChoices):
        ASSIGNED = "assigned", "Assigned"
        ACCEPTED = "accepted", "Accepted"
        STARTED = "started", "Started"
        PAUSED = "paused", "Paused"
        RESUMED = "resumed", "Resumed"
        COMPLETED = "completed", "Completed"
        FAILED_INSPECTION = "failed_inspection", "Failed Inspection"
        REOPENED = "reopened", "Reopened"
        CANCELLED = "cancelled", "Cancelled"


    class ChangeSource(models.TextChoices):
        USER = "user", "User"
        SYSTEM = "system", "System"
        AUTOMATION = "automation", "Automation"
        INSPECTION = "inspection", "Inspection"


    assignment = models.ForeignKey(
        HousekeepingAssignment,
        on_delete=models.CASCADE,
        related_name="status_logs",
    )


    previous_status = models.CharField(
        max_length=30,
        choices=Status.choices,
        blank=True,
    )


    new_status = models.CharField(
        max_length=30,
        choices=Status.choices,
    )


    changed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="housekeeping_status_changes",
    )


    change_source = models.CharField(
        max_length=20,
        choices=ChangeSource.choices,
        default=ChangeSource.USER,
    )


    remarks = models.TextField(
        blank=True,
    )


    metadata = models.JSONField(
        default=dict,
        blank=True,
    )


    class Meta:

        ordering = [
            "-created_at",
        ]

        indexes = [

            models.Index(
                fields=[
                    "assignment",
                    "created_at",
                ],
                name="idx_hk_status_assignment_date",
            ),

            models.Index(
                fields=[
                    "new_status",
                ],
                name="idx_hk_status_new",
            ),

            models.Index(
                fields=[
                    "change_source",
                ],
                name="idx_hk_status_source",
            ),

        ]

    def __str__(self):
        return (
            f"{self.assignment.task.title}: "
            f"{self.previous_status} → {self.new_status}"
        )