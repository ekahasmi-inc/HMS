from django.db import models

from apps.operations.booking.models import Property, Room
from apps.platform.common.models import TimeStampedModel


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