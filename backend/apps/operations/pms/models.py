from django.db import models
from django.conf import settings
from django.utils import timezone
from apps.platform.common.models import TimeStampedModel
from apps.operations.booking.models import Reservation, Property, Guest, Room, ReservationRoom
from apps.experience.assets.models import MediaReference
from django.core.exceptions import ValidationError


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



class RoomMove(TimeStampedModel):
    """
    Records an operational movement of a reservation from one
    physical room to another.

    RoomAssignment remains the source of truth for room allocation.
    RoomMove records the operational event/change.
    """
    class MoveReason(models.TextChoices):
        GUEST_REQUEST = "guest_request", "Guest Request"
        MAINTENANCE = "maintenance", "Maintenance"
        ROOM_UNAVAILABLE = "room_unavailable", "Room Unavailable"
        UPGRADE = "upgrade", "Upgrade"
        DOWNGRADE = "downgrade", "Downgrade"
        OPERATIONAL = "operational", "Operational"
        OVERBOOKING = "overbooking", "Overbooking"
        HOUSEKEEPING = "housekeeping", "Housekeeping"
        OTHER = "other", "Other"

    class ChangeType(models.TextChoices):
        SAME_CATEGORY = "same_category", "Same Category"
        UPGRADE = "upgrade", "Upgrade"
        DOWNGRADE = "downgrade", "Downgrade"

    class InitiatedBy(models.TextChoices):
        GUEST = "guest", "Guest"
        STAFF = "staff", "Staff"
        SYSTEM = "system", "System"
        AI = "ai", "AI Assisted"

    class Status(models.TextChoices):
        REQUESTED = "requested", "Requested"
        APPROVED = "approved", "Approved"
        COMPLETED = "completed", "Completed"
        CANCELLED = "cancelled", "Cancelled"

    reservation = models.ForeignKey(Reservation, on_delete=models.CASCADE, related_name="room_moves",)
    reservation_room = models.ForeignKey(ReservationRoom, on_delete=models.CASCADE, related_name="room_moves",)
    previous_assignment = models.ForeignKey(RoomAssignment, on_delete=models.PROTECT, related_name="moves_from",)
    new_assignment = models.ForeignKey(RoomAssignment, on_delete=models.PROTECT, related_name="moves_to",)
    previous_room = models.ForeignKey(Room, on_delete=models.PROTECT, related_name="room_moves_from",)
    new_room = models.ForeignKey(Room,on_delete=models.PROTECT, related_name="room_moves_to",)
    initiated_by = models.CharField(max_length=20, choices=InitiatedBy.choices, default=InitiatedBy.STAFF,)
    authorized_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name="authorized_room_moves",)
    status = models.CharField(max_length=20,choices=Status.choices,default=Status.REQUESTED,)
    reason = models.CharField(max_length=30, choices=MoveReason.choices, default=MoveReason.OPERATIONAL,)
    change_type = models.CharField(max_length=30, choices=ChangeType.choices, default=ChangeType.SAME_CATEGORY,)
    effective_at = models.DateTimeField(null=True, blank=True,)
    requested_at = models.DateTimeField(auto_now_add=True,)
    completed_at = models.DateTimeField(null=True, blank=True,)
    notes = models.TextField(blank=True,)
    metadata = models.JSONField(default=dict, blank=True,)

    class Meta:
        ordering = ["-effective_at", "-created_at",]

        indexes = [
            models.Index(
                fields=["reservation", "status",],
                name="idx_roommove_res_status",
            ),
            models.Index(
                fields=["reservation_room", "effective_at",],
                name="idx_roommove_resroom_date",
            ),
            models.Index(
                fields=["previous_room", "effective_at",],
                name="idx_roommove_prevroom_date",
            ),
            models.Index(
                fields=["new_room", "effective_at",],
                name="idx_roommove_newroom_date",
            ),
            models.Index(
                fields=["status", "effective_at",],
                name="idx_roommove_status_date",
            ),
        ]

    def clean(self):
        errors = {}

        if self.reservation_room:
            if self.reservation_room.reservation_id != self.reservation_id:
                errors["reservation_room"] = (
                    "ReservationRoom must belong to the selected reservation."
                )

        if self.previous_assignment:
            if (
                self.previous_assignment.reservation_room_id
                != self.reservation_room_id
            ):
                errors["previous_assignment"] = (
                    "Previous assignment must belong to the selected ReservationRoom."
                )

        if self.new_assignment:
            if (
                self.new_assignment.reservation_room_id
                != self.reservation_room_id
            ):
                errors["new_assignment"] = (
                    "New assignment must belong to the selected ReservationRoom."
                )

        if self.previous_assignment and self.previous_room:
            if self.previous_assignment.room_id != self.previous_room_id:
                errors["previous_room"] = (
                    "Previous room must match the previous assignment."
                )

        if self.new_assignment and self.new_room:
            if self.new_assignment.room_id != self.new_room_id:
                errors["new_room"] = (
                    "New room must match the new assignment."
                )

        if (
            self.previous_room_id
            and self.new_room_id
            and self.previous_room_id == self.new_room_id
        ):
            errors["new_room"] = (
                "New room must be different from the previous room."
            )

        if errors:
           raise ValidationError(errors)
        
    def __str__(self):
        return (
            f"{self.reservation_room} - "
            f"{self.previous_room} → {self.new_room}"
        )


class GuestDocument(TimeStampedModel):
    """
    Identity document belonging to a guest.

    GuestDocument stores document metadata and verification state.
    Actual document files are referenced through MediaReference.
    """

    class DocumentType(models.TextChoices):
        PASSPORT = "passport", "Passport"
        AADHAAR = "aadhaar", "Aadhaar"
        PAN = "pan", "PAN"
        DRIVING_LICENSE = "driving_license", "Driving License"
        VOTER_ID = "voter_id", "Voter ID"
        NATIONAL_ID = "national_id", "National ID"
        OTHER = "other", "Other"

    class VerificationStatus(models.TextChoices):
        PENDING = "pending", "Pending"
        VERIFIED = "verified", "Verified"
        REJECTED = "rejected", "Rejected"
        EXPIRED = "expired", "Expired"

    guest = models.ForeignKey(
        Guest,
        on_delete=models.CASCADE,
        related_name="documents",
    )

    document_type = models.CharField(
        max_length=30,
        choices=DocumentType.choices,
    )

    document_number = models.CharField(
        max_length=100,
    )

    issuing_country = models.CharField(
        max_length=100,
        blank=True,
    )

    issue_date = models.DateField(
        null=True,
        blank=True,
    )

    expiry_date = models.DateField(
        null=True,
        blank=True,
    )

    verification_status = models.CharField(
        max_length=20,
        choices=VerificationStatus.choices,
        default=VerificationStatus.PENDING,
    )

    verified_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    verified_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="guest_documents_verified",
    )

    media_reference = models.ForeignKey(
        MediaReference,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="guest_documents",
    )

    metadata = models.JSONField(
        default=dict,
        blank=True,
    )

    notes = models.TextField(
        blank=True,
    )

    class Meta:
        ordering = [
            "-created_at",
        ]

        constraints = [
            models.UniqueConstraint(
                fields=[
                    "guest",
                    "document_type",
                    "document_number",
                ],
                name="uq_guest_document_identity",
            ),
        ]

        indexes = [
            models.Index(
                fields=[
                    "guest",
                    "document_type",
                ],
                name="idx_guestdoc_guest_type",
            ),

            models.Index(
                fields=[
                    "guest",
                    "verification_status",
                ],
                name="idx_guestdoc_guest_status",
            ),

            models.Index(
                fields=[
                    "document_number",
                ],
                name="idx_guestdoc_number",
            ),

            models.Index(
                fields=[
                    "expiry_date",
                ],
                name="idx_guestdoc_expiry",
            ),
        ]

    def clean(self):
        errors = {}

        if (
            self.issue_date
            and self.expiry_date
            and self.expiry_date < self.issue_date
        ):
            errors["expiry_date"] = (
                "Expiry date cannot be earlier than issue date."
            )

        if (
            self.verification_status
            == self.VerificationStatus.VERIFIED
            and not self.verified_at
        ):
            errors["verified_at"] = (
                "Verified timestamp is required for verified documents."
            )

        if (
            self.verification_status
            == self.VerificationStatus.VERIFIED
            and not self.verified_by
        ):
            errors["verified_by"] = (
                "Verified by is required for verified documents."
            )

        if errors:
            raise ValidationError(errors)

    def __str__(self):
        return (
            f"{self.guest} - "
            f"{self.get_document_type_display()} - "
            f"{self.document_number}"
        )


class KeyCard(TimeStampedModel):
    """
    Represents a physical or electronic room-access credential.

    KeyCard belongs to the PMS access layer and does not contain
    reservation pricing, payment, or booking logic.
    """

    class CardType(models.TextChoices):
        PHYSICAL = "physical", "Physical Card"
        RFID = "rfid", "RFID Card"
        NFC = "nfc", "NFC Credential"
        MOBILE = "mobile", "Mobile Key"
        DIGITAL = "digital", "Digital Credential"
        OTHER = "other", "Other"

    class Status(models.TextChoices):
        ISSUED = "issued", "Issued"
        ACTIVE = "active", "Active"
        EXPIRED = "expired", "Expired"
        RETURNED = "returned", "Returned"
        DEACTIVATED = "deactivated", "Deactivated"
        LOST = "lost", "Lost"
        DAMAGED = "damaged", "Damaged"
        CANCELLED = "cancelled", "Cancelled"

    reservation = models.ForeignKey(
        Reservation,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="key_cards",
    )

    guest = models.ForeignKey(
        Guest,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="key_cards",
    )

    check_in = models.ForeignKey(
        CheckIn,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="key_cards",
    )

    room = models.ForeignKey(
        Room,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="key_cards",
    )

    credential_number = models.CharField(
        max_length=100,
        unique=True,
    )

    card_type = models.CharField(
        max_length=20,
        choices=CardType.choices,
        default=CardType.PHYSICAL,
    )

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.ISSUED,
    )

    issued_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    activated_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    expires_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    deactivated_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    returned_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    issued_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="key_cards_issued",
    )

    returned_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="key_cards_returned",
    )

    notes = models.TextField(
        blank=True,
    )

    metadata = models.JSONField(
        default=dict,
        blank=True,
    )

    class Meta:
        ordering = [
            "-issued_at",
            "-created_at",
        ]

        indexes = [
            models.Index(
                fields=[
                    "reservation",
                    "status",
                ],
                name="idx_keycard_res_status",
            ),

            models.Index(
                fields=[
                    "guest",
                    "status",
                ],
                name="idx_keycard_guest_status",
            ),

            models.Index(
                fields=[
                    "room",
                    "status",
                ],
                name="idx_keycard_room_status",
            ),

            models.Index(
                fields=[
                    "check_in",
                ],
                name="idx_keycard_checkin",
            ),

            models.Index(
                fields=[
                    "status",
                    "expires_at",
                ],
                name="idx_keycard_status_expiry",
            ),
        ]

    def clean(self):
        errors = {}

        if self.expires_at and self.issued_at:
            if self.expires_at < self.issued_at:
                errors["expires_at"] = (
                    "Expiry time cannot be earlier than issue time."
                )

        if self.activated_at and self.issued_at:
            if self.activated_at < self.issued_at:
                errors["activated_at"] = (
                    "Activation time cannot be earlier than issue time."
                )

        if self.returned_at and self.issued_at:
            if self.returned_at < self.issued_at:
                errors["returned_at"] = (
                    "Return time cannot be earlier than issue time."
                )

        if (
            self.status == self.Status.RETURNED
            and not self.returned_at
        ):
            errors["returned_at"] = (
                "Returned timestamp is required for returned cards."
            )

        if (
            self.status == self.Status.DEACTIVATED
            and not self.deactivated_at
        ):
            errors["deactivated_at"] = (
                "Deactivation timestamp is required for deactivated cards."
            )

        if errors:
            raise ValidationError(errors)

    def __str__(self):
        if self.room:
            room_display = (
                f"{self.room.room_number} - {self.room.room_name}"
            )
        else:
            room_display = "Unassigned Room"

        return f"{self.credential_number} - {room_display}"