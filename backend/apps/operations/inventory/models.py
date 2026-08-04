from django.db import models
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