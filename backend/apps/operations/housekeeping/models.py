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



from decimal import Decimal


class MaintenanceRequest(TimeStampedModel):
    """
    Maintenance work request for rooms, buildings and property assets.
    """

    class Category(models.TextChoices):
        ELECTRICAL = "electrical", "Electrical"
        PLUMBING = "plumbing", "Plumbing"
        HVAC = "hvac", "HVAC / Air Conditioning"
        CIVIL = "civil", "Civil"
        PAINTING = "painting", "Painting"
        FURNITURE = "furniture", "Furniture"
        APPLIANCE = "appliance", "Appliance"
        IT = "it", "IT / Network"
        LANDSCAPING = "landscaping", "Landscaping"
        SAFETY = "safety", "Safety"
        OTHER = "other", "Other"


    class Priority(models.TextChoices):
        LOW = "low", "Low"
        NORMAL = "normal", "Normal"
        HIGH = "high", "High"
        CRITICAL = "critical", "Critical"


    class RequestType(models.TextChoices):
        PREVENTIVE = "preventive", "Preventive"
        CORRECTIVE = "corrective", "Corrective"
        EMERGENCY = "emergency", "Emergency"
        INSPECTION = "inspection", "Inspection"


    class Status(models.TextChoices):
        OPEN = "open", "Open"
        APPROVED = "approved", "Approved"
        IN_PROGRESS = "in_progress", "In Progress"
        ON_HOLD = "on_hold", "On Hold"
        COMPLETED = "completed", "Completed"
        CANCELLED = "cancelled", "Cancelled"


    property = models.ForeignKey(
        Property,
        on_delete=models.CASCADE,
        related_name="maintenance_requests",
    )


    building = models.ForeignKey(
        "booking.Building",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="maintenance_requests",
    )


    floor = models.ForeignKey(
        "booking.Floor",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="maintenance_requests",
    )


    room = models.ForeignKey(
        Room,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="maintenance_requests",
    )


    housekeeping_task = models.ForeignKey(
        HousekeepingTask,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="maintenance_requests",
    )


    title = models.CharField(
        max_length=200,
    )


    description = models.TextField(
        blank=True,
    )


    category = models.CharField(
        max_length=30,
        choices=Category.choices,
    )


    request_type = models.CharField(
        max_length=30,
        choices=RequestType.choices,
        default=RequestType.CORRECTIVE,
    )


    priority = models.CharField(
        max_length=20,
        choices=Priority.choices,
        default=Priority.NORMAL,
    )


    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.OPEN,
    )


    reported_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="maintenance_requests_reported",
    )


    approved_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="maintenance_requests_approved",
    )


    scheduled_date = models.DateField(
        null=True,
        blank=True,
    )


    estimated_duration_minutes = models.PositiveIntegerField(
        default=60,
    )


    estimated_cost = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal("0.00"),
    )


    metadata = models.JSONField(
        default=dict,
        blank=True,
    )


    class Meta:

        ordering = [
            "-priority",
            "-created_at",
        ]

        constraints = [

            models.UniqueConstraint(
                fields=[
                    "property",
                    "title",
                    "created_at",
                ],
                name="uq_maintenance_request_unique",
            ),

        ]

        indexes = [

            models.Index(
                fields=[
                    "property",
                    "status",
                ],
                name="idx_maint_property_status",
            ),

            models.Index(
                fields=[
                    "room",
                    "status",
                ],
                name="idx_maint_room_status",
            ),

            models.Index(
                fields=[
                    "priority",
                    "status",
                ],
                name="idx_maint_priority_status",
            ),

        ]


    def __str__(self):

        return f"{self.property.name} - {self.title}"



from decimal import Decimal
from django.conf import settings


class MaintenanceLog(TimeStampedModel):
    """
    Execution log for maintenance work.
    """

    class WorkStatus(models.TextChoices):
        STARTED = "started", "Started"
        IN_PROGRESS = "in_progress", "In Progress"
        PAUSED = "paused", "Paused"
        COMPLETED = "completed", "Completed"
        FAILED = "failed", "Failed"
        CANCELLED = "cancelled", "Cancelled"


    request = models.ForeignKey(
        MaintenanceRequest,
        on_delete=models.CASCADE,
        related_name="logs",
    )


    technician = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="maintenance_logs",
    )


    work_status = models.CharField(
        max_length=20,
        choices=WorkStatus.choices,
        default=WorkStatus.STARTED,
    )


    work_started_at = models.DateTimeField(
        null=True,
        blank=True,
    )


    work_completed_at = models.DateTimeField(
        null=True,
        blank=True,
    )


    labor_hours = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        default=Decimal("0.00"),
    )


    materials_used = models.JSONField(
        default=list,
        blank=True,
        help_text="List of parts/materials used.",
    )


    labor_cost = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal("0.00"),
    )


    material_cost = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal("0.00"),
    )


    total_cost = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal("0.00"),
    )


    before_notes = models.TextField(
        blank=True,
    )


    work_performed = models.TextField(
        blank=True,
    )


    after_notes = models.TextField(
        blank=True,
    )


    completion_evidence = models.JSONField(
        default=dict,
        blank=True,
        help_text="References to photos, videos, documents, invoices, etc.",
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
                    "request",
                    "created_at",
                ],
                name="idx_maint_log_request_date",
            ),

            models.Index(
                fields=[
                    "technician",
                    "work_status",
                ],
                name="idx_maint_log_tech_status",
            ),

        ]


    def save(self, *args, **kwargs):

        self.total_cost = (
            self.labor_cost +
            self.material_cost
        )

        super().save(*args, **kwargs)


    def __str__(self):

        return (
            f"{self.request.title} - "
            f"{self.work_status}"
        )



class CleaningChecklist(TimeStampedModel):
    """
    Reusable cleaning procedure definition.
    """

    class ChecklistType(models.TextChoices):

        ROOM_CLEANING = "room_cleaning", "Room Cleaning"
        CHECKOUT = "checkout", "Checkout Cleaning"
        DEEP_CLEANING = "deep_cleaning", "Deep Cleaning"
        PUBLIC_AREA = "public_area", "Public Area"
        RESTAURANT = "restaurant", "Restaurant"
        EVENT = "event", "Event Cleanup"
        OTHER = "other", "Other"


    class Status(models.TextChoices):

        DRAFT = "draft", "Draft"
        ACTIVE = "active", "Active"
        INACTIVE = "inactive", "Inactive"


    property = models.ForeignKey(
        Property,
        on_delete=models.CASCADE,
        related_name="cleaning_checklists",
    )


    name = models.CharField(
        max_length=200,
    )


    slug = models.SlugField(
        max_length=200,
    )


    checklist_type = models.CharField(
        max_length=30,
        choices=ChecklistType.choices,
        default=ChecklistType.ROOM_CLEANING,
    )


    description = models.TextField(
        blank=True,
    )


    version = models.PositiveIntegerField(
        default=1,
    )


    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.DRAFT,
    )


    is_default = models.BooleanField(
        default=False,
    )


    metadata = models.JSONField(
        default=dict,
        blank=True,
    )


    class Meta:

        ordering = [
            "name",
        ]


        constraints = [

            models.UniqueConstraint(
                fields=[
                    "property",
                    "slug",
                    "version",
                ],
                name="uq_cleaning_checklist_property_version",
            ),

        ]


        indexes = [

            models.Index(
                fields=[
                    "property",
                    "status",
                ],
                name="idx_cleaning_checklist_status",
            ),

            models.Index(
                fields=[
                    "property",
                    "checklist_type",
                ],
                name="idx_cleaning_checklist_type",
            ),

        ]


    def __str__(self):

        return f"{self.property.name} - {self.name}"