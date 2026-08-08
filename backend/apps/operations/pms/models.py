from django.db import models
from django.conf import settings
from django.utils import timezone
from apps.platform.common.models import TimeStampedModel
from apps.operations.booking.models import Reservation, Property, Guest, Room, ReservationRoom


class CheckIn(TimeStampedModel):
    """
    Records the operational guest arrival.
    """

    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        CHECKED_IN = "checked_in", "Checked In"
        CANCELLED = "cancelled", "Cancelled"
        NO_SHOW = "no_show", "No Show"

    reservation = models.OneToOneField(Reservation, on_delete=models.CASCADE, related_name="checkin_record",)
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name="check_ins",)
    guest = models.ForeignKey(Guest, on_delete=models.CASCADE, related_name="check_ins",)
    checked_in_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name="processed_check_ins",)
    actual_check_in = models.DateTimeField(default=timezone.now,)
    expected_check_out = models.DateTimeField()
    adults = models.PositiveIntegerField(default=1,)
    children = models.PositiveIntegerField(default=0,)
    security_deposit = models.DecimalField(max_digits=12, decimal_places=2, default=0,)
    status = models.CharField(max_length=30, choices=Status.choices, default=Status.PENDING,)
    remarks = models.TextField(blank=True,)
    metadata = models.JSONField(default=dict, blank=True,)

    class Meta:
        ordering = ["-actual_check_in",]

        constraints = [
            models.UniqueConstraint(
                fields=["reservation",],
                name="uq_checkin_reservation",
            ),
        ]
        indexes = [
            models.Index(
                fields=["property", "status",],
                name="idx_checkin_property_status",
            ),
            models.Index(
                fields=["guest",],
                name="idx_checkin_guest",
            ),
        ]

    def __str__(self):
        return (
            f"{self.reservation.booking_number}"
            f" - Check-In"
        )


from django.conf import settings
from django.utils import timezone


class CheckOut(TimeStampedModel):
    """
    Records the operational guest departure.
    """
    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        CHECKED_OUT = "checked_out", "Checked Out"
        LATE_CHECKOUT = "late_checkout", "Late Checkout"
        EARLY_CHECKOUT = "early_checkout", "Early Checkout"

    class InspectionStatus(models.TextChoices):
        PENDING = "pending", "Pending"
        PASSED = "passed", "Passed"
        FAILED = "failed", "Failed"

    check_in = models.OneToOneField(CheckIn, on_delete=models.CASCADE, related_name="check_out",)
    reservation = models.OneToOneField(Reservation, on_delete=models.CASCADE, related_name="pms_check_out",)
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name="check_outs",)
    processed_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,  null=True, blank=True, related_name="processed_check_outs",)
    actual_check_out = models.DateTimeField(default=timezone.now,)
    status = models.CharField(max_length=30, choices=Status.choices, default=Status.PENDING,)
    inspection_status = models.CharField(max_length=20, choices=InspectionStatus.choices, default=InspectionStatus.PENDING,)
    housekeeping_required = models.BooleanField(default=True,)
    room_ready_for_sale = models.BooleanField(default=False,)
    final_bill_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0,)
    deposit_collected = models.DecimalField(max_digits=12, decimal_places=2, default=0,)
    deposit_refunded = models.DecimalField(max_digits=12, decimal_places=2, default=0,)
    additional_charges = models.DecimalField(max_digits=12,decimal_places=2,default=0,)
    guest_feedback_score = models.PositiveSmallIntegerField(null=True, blank=True,)
    guest_feedback = models.TextField(blank=True,)
    remarks = models.TextField(blank=True,)
    metadata = models.JSONField(default=dict, blank=True,)

    class Meta:
        ordering = ["-actual_check_out",]

        constraints = [
            models.UniqueConstraint(
                fields=["check_in",],
                name="uq_checkout_checkin",
            ),
            models.UniqueConstraint(
                fields=["reservation",],
                name="uq_checkout_reservation",
            ),
        ]

        indexes = [
            models.Index(
                fields=["property","status",],
                name="idx_checkout_property_status",
            ),
            models.Index(
                fields=["actual_check_out",],
                name="idx_checkout_date",
            ),
        ]

    def __str__(self):
        return (
            f"{self.reservation.booking_number}"
            f" - Check-Out"
        )



class RoomAssignment(TimeStampedModel):
    """
    Represents the allocation of a physical room to a ReservationRoom.

    ReservationRoom = what the guest booked.
    RoomAssignment = the physical room actually allocated.
    """
    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        ASSIGNED = "assigned", "Assigned"
        ACTIVE = "active", "Active"
        RELEASED = "released", "Released"
        CANCELLED = "cancelled", "Cancelled"

    class AssignmentMethod(models.TextChoices):
        MANUAL = "manual", "Manual"
        AUTOMATIC = "automatic", "Automatic"
        AI = "ai", "AI Assisted"

    class ChangeType(models.TextChoices):
        NONE = "none", "No Change"
        UPGRADE = "upgrade", "Upgrade"
        DOWNGRADE = "downgrade", "Downgrade"
        ROOM_CHANGE = "room_change", "Room Change"

    reservation_room = models.ForeignKey(ReservationRoom, on_delete=models.CASCADE, related_name="room_assignments",)
    room = models.ForeignKey(Room, on_delete=models.PROTECT, related_name="room_assignments",)
    assigned_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name="room_assignments_created",)
    status = models.CharField(max_length=30, choices=Status.choices, default=Status.PENDING,)
    assignment_method = models.CharField(max_length=30, choices=AssignmentMethod.choices, default=AssignmentMethod.MANUAL,)
    change_type = models.CharField( max_length=30, choices=ChangeType.choices,  default=ChangeType.NONE,)
    assigned_at = models.DateTimeField(null=True, blank=True,)
    effective_from = models.DateTimeField(null=True, blank=True,)
    effective_until = models.DateTimeField(null=True, blank=True,)
    assignment_reason = models.CharField(max_length=255,blank=True,)
    notes = models.TextField(blank=True,)
    metadata = models.JSONField(default=dict, blank=True,)

    class Meta:
        ordering = ["-assigned_at", "-created_at",]

        indexes = [
            models.Index(
                fields=["reservation_room", "status",],
                name="idx_roomassign_resroom_status",
            ),
            models.Index(
                fields=["room", "status",],
                name="idx_roomassign_room_status",
            ),
            models.Index(
                fields=["effective_from", "effective_until",],
                name="idx_roomassign_effectiv_period",
            ),
        ]

    def __str__(self):
        return (
            f"{self.reservation_room} → "
            f"{self.room}"
        )