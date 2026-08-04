from django.db import models
from django.conf import settings
from apps.platform.common.models import TimeStampedModel
from apps.operations.booking.models import Room

class InventoryCalendar(TimeStampedModel):
    """
    Daily inventory availability for a physical room.
    """
    class InventoryStatus(models.TextChoices):
        AVAILABLE = "available", "Available"
        RESERVED = "reserved", "Reserved"
        OCCUPIED = "occupied", "Occupied"
        BLOCKED = "blocked", "Blocked"
        MAINTENANCE = "maintenance", "Maintenance"
        OUT_OF_ORDER = "out_of_order", "Out of Order"

    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name="inventory_calendar",)
    date = models.DateField()
    status = models.CharField(max_length=30, choices=InventoryStatus.choices, default=InventoryStatus.AVAILABLE,)
    is_available = models.BooleanField(default=True,)
    inventory_count = models.PositiveIntegerField(default=1,)
    available_count = models.PositiveIntegerField(default=1,)
    minimum_stay = models.PositiveSmallIntegerField(default=1,)
    maximum_stay = models.PositiveSmallIntegerField(default=30,)
    closed_to_arrival = models.BooleanField(default=False,)
    closed_to_departure = models.BooleanField(default=False,)
    metadata = models.JSONField(default=dict, blank=True,)

    class Meta:
        ordering = ["date", "room",]

        constraints = [
            models.UniqueConstraint(
                fields=["room", "date"],
                name="uq_inventory_calendar_room_date",
            ),
        ]

        indexes = [
            models.Index(
                fields=["room", "date"],
                name="idx_inventory_room_date",
            ),
            models.Index(
                fields=["date", "status"],
                name="idx_inventory_date_status",
            ),
            models.Index(
                fields=["status", "is_available"],
                name="idx_inventory_status_available",
            ),
        ]

    def __str__(self):
        return f"{self.room.room_number} - {self.date}"


class InventoryBlock(TimeStampedModel):
    """
    Blocks room inventory for a date range.
    """
    class BlockType(models.TextChoices):
        MAINTENANCE = "maintenance", "Maintenance"
        OWNER_STAY = "owner_stay", "Owner Stay"
        VIP_HOLD = "vip_hold", "VIP Hold"
        GROUP_HOLD = "group_hold", "Group Hold"
        HOUSEKEEPING = "housekeeping", "Housekeeping"
        RENOVATION = "renovation", "Renovation"
        EMERGENCY = "emergency", "Emergency"
        OTHER = "other", "Other"

    class BlockStatus(models.TextChoices):
        ACTIVE = "active", "Active"
        CANCELLED = "cancelled", "Cancelled"
        COMPLETED = "completed", "Completed"

    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name="inventory_blocks",)
    block_type = models.CharField(max_length=40, choices=BlockType.choices,)
    title = models.CharField( max_length=200,)
    description = models.TextField(blank=True,)
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(max_length=20, choices=BlockStatus.choices, default=BlockStatus.ACTIVE,)
    blocks_arrival = models.BooleanField(default=True,)
    blocks_departure = models.BooleanField(default=True,)
    blocks_inventory = models.BooleanField(default=True,)
    metadata = models.JSONField(default=dict, blank=True,)

    class Meta:

        ordering = [
            "-start_date",
            "room",
        ]

        indexes = [

            models.Index(
                fields=["room", "start_date"],
                name="idx_block_room_start",
            ),

            models.Index(
                fields=["start_date", "end_date"],
                name="idx_block_dates",
            ),

            models.Index(
                fields=["status", "block_type"],
                name="idx_block_status_type",
            ),

        ]

    def __str__(self):
        return f"{self.room.room_number} | {self.title}"


class InventoryAdjustment(TimeStampedModel):
    """
    Audit log for inventory changes.
    """
    class AdjustmentType(models.TextChoices):
        MANUAL = "manual", "Manual"
        BOOKING = "booking", "Booking"
        OTA_SYNC = "ota_sync", "OTA Sync"
        HOUSEKEEPING = "housekeeping", "Housekeeping"
        MAINTENANCE = "maintenance", "Maintenance"
        AI = "ai", "AI Recommendation"
        SYSTEM = "system", "System"
        OTHER = "other", "Other"

    inventory = models.ForeignKey(InventoryCalendar, on_delete=models.CASCADE, related_name="adjustments",)
    adjustment_type = models.CharField(max_length=30, choices=AdjustmentType.choices,)
    previous_status = models.CharField(max_length=30, choices=InventoryCalendar.InventoryStatus.choices,)
    new_status = models.CharField(max_length=30, choices=InventoryCalendar.InventoryStatus.choices,)
    previous_available_count = models.PositiveIntegerField()
    new_available_count = models.PositiveIntegerField()
    reason = models.CharField(max_length=255,)
    notes = models.TextField(blank=True,)
    adjusted_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name="inventory_adjustments",)
    reference_id = models.CharField(max_length=100, blank=True, help_text="Booking ID / OTA ID / Ticket ID / External Reference",)
    metadata = models.JSONField(default=dict, blank=True,)

    class Meta:
        ordering = ["-created_at",]

        indexes = [
            models.Index(
                fields=["inventory"],
                name="idx_adjustment_inventory",
            ),
            models.Index(
                fields=["adjustment_type"],
                name="idx_adjustment_type",
            ),
            models.Index(
                fields=["created_at"],
                name="idx_adjustment_created",
            ),
        ]

    def __str__(self):
        return (
            f"{self.inventory.room.room_number} | "
            f"{self.adjustment_type} | "
            f"{self.created_at:%Y-%m-%d %H:%M}"
        )