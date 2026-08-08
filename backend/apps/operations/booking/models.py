from django.db import models
from django.conf import settings
from apps.platform.common.models import TimeStampedModel
from apps.platform.tenants.models import Tenant
from apps.platform.common.models import BaseModel
from django.utils.text import slugify


class Property(BaseModel):
    """
    Physical property owned by a tenant.
    """

    class PropertyType(models.TextChoices):
        HOTEL = "hotel", "Hotel"
        RESORT = "resort", "Resort"
        VILLA = "villa", "Villa"
        HOMESTAY = "homestay", "Homestay"
        APARTMENT = "apartment", "Apartment"
        HOSTEL = "hostel", "Hostel"
        CAMP = "camp", "Camp"
        OTHER = "other", "Other"

    class Status(models.TextChoices):
        DRAFT = "draft", "Draft"
        ACTIVE = "active", "Active"
        INACTIVE = "inactive", "Inactive"
        CLOSED = "closed", "Closed"

    tenant = models.ForeignKey("tenants.Tenant", on_delete=models.CASCADE, related_name="properties",)
    name = models.CharField(max_length=255,)
    slug = models.SlugField(max_length=255,)
    property_type = models.CharField(max_length=30, choices=PropertyType.choices, default=PropertyType.RESORT,)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.DRAFT,)
    description = models.TextField(blank=True,)
    email = models.EmailField(blank=True,)
    phone = models.CharField(max_length=30, blank=True,)
    website = models.URLField(blank=True,)
    address_line_1 = models.CharField(max_length=255, blank=True,)
    address_line_2 = models.CharField(max_length=255, blank=True,)
    city = models.CharField(max_length=100, blank=True,)
    state = models.CharField(max_length=100, blank=True,)
    country = models.CharField(max_length=100, blank=True,)
    postal_code = models.CharField(max_length=20, blank=True,)
    latitude = models.DecimalField(max_digits=10, decimal_places=7, null=True, blank=True,)
    longitude = models.DecimalField(max_digits=10, decimal_places=7, null=True, blank=True,)
    timezone = models.CharField(max_length=100, default="Asia/Kolkata",)
    currency = models.CharField(max_length=10, default="INR",)
    star_rating = models.PositiveSmallIntegerField(default=0,)
    metadata = models.JSONField(default=dict, blank=True,)

    class Meta:
        ordering = ["name"]

        constraints = [
            models.UniqueConstraint(
                fields=["tenant", "slug"],
                name="uq_property_tenant_slug",
            ),
            models.UniqueConstraint(
                fields=["tenant", "name"],
                name="uq_property_tenant_name",
            ),
        ]

        indexes = [
            models.Index(
                fields=["tenant", "status"],
                name="idx_property_tenant_status",
            ),
            models.Index(
                fields=["property_type"],
                name="idx_property_type",
            ),
        ]

    def __str__(self):
        return self.name


class PropertyAmenity(BaseModel):
    """
    Property-level facilities and services.
    """
    class Category(models.TextChoices):
        GENERAL = "general", "General"
        DINING = "dining", "Dining"
        WELLNESS = "wellness", "Wellness"
        RECREATION = "recreation", "Recreation"
        BUSINESS = "business", "Business"
        TRANSPORT = "transport", "Transport"
        ACCESSIBILITY = "accessibility", "Accessibility"
        SAFETY = "safety", "Safety"
        OTHER = "other", "Other"

    property = models.ForeignKey("Property", on_delete=models.CASCADE, related_name="amenities",)
    name = models.CharField(max_length=150,)
    slug = models.SlugField(max_length=150,)
    category = models.CharField(max_length=30, choices=Category.choices, default=Category.GENERAL,)
    description = models.TextField(blank=True,)
    icon = models.CharField(max_length=100, blank=True, help_text="Icon name (Font Awesome, Material Icons, etc.)",)
    display_order = models.PositiveIntegerField(default=1,)
    is_featured = models.BooleanField(default=False,)
    is_active = models.BooleanField(default=True,)
    metadata = models.JSONField(default=dict, blank=True,)

    class Meta:
        ordering = ("display_order","name",)

        constraints = [
            models.UniqueConstraint(
                fields=["property","slug",],
                name="uq_property_amenity_slug",
            ),
            models.UniqueConstraint(
                fields=["property","name",],
                name="uq_property_amenity_name",
            ),
        ]

        indexes = [
            models.Index(
                fields=["property","is_active",],
                name="idx_prop_amn_active",
            ),
            models.Index(
                fields=["category",],
                name="idx_prop_amn_cat",
            ),
        ]

    def __str__(self):
        return f"{self.property.name} - {self.name}"


class Building(TimeStampedModel):
    """
    Physical building within a property.
    """
    class BuildingType(models.TextChoices):

        MAIN = "main", "Main Building"
        VILLA = "villa", "Villa"
        BLOCK = "block", "Block"
        COTTAGE = "cottage", "Cottage"
        OTHER = "other", "Other"

    class BuildingStatus(models.TextChoices):
        ACTIVE = "active", "Active"
        INACTIVE = "inactive", "Inactive"
        UNDER_CONSTRUCTION = "under_construction", "Under Construction"
        CLOSED = "closed", "Closed"

    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name="buildings",)
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200)
    code = models.CharField(max_length=30, blank=True,)
    building_type = models.CharField(max_length=30, choices=BuildingType.choices, default=BuildingType.MAIN,)
    description = models.TextField(blank=True,)
    building_number = models.CharField(max_length=50, blank=True,)
    total_floors = models.PositiveIntegerField(default=1,)
    status = models.CharField(max_length=30, choices=BuildingStatus.choices, default=BuildingStatus.ACTIVE,)
    sort_order = models.PositiveIntegerField(default=0,)
    metadata = models.JSONField(default=dict, blank=True,)

    class Meta:
        ordering = ["sort_order", "name",]

        constraints = [
            models.UniqueConstraint(
                fields=["property", "slug"],
                name="uq_building_property_slug",
            ),
            models.UniqueConstraint(
                fields=["property", "name"],
                name="uq_building_property_name",
            ),
        ]

        indexes = [
            models.Index(
                fields=["property", "status"],
                name="idx_building_property_status",
            ),
            models.Index(
                fields=["property", "sort_order"],
                name="idx_building_property_order",
            ),
        ]

    def __str__(self):
        return f"{self.property.name} - {self.name}"


class Floor(TimeStampedModel):
    """
    Physical floor within a building.
    """
    class FloorType(models.TextChoices):

        BASEMENT = "basement", "Basement"
        GROUND = "ground", "Ground Floor"
        FIRST = "first", "First Floor"
        SECOND = "second", "Second Floor"
        THIRD = "third", "Third Floor"
        TERRACE = "terrace", "Terrace"
        OTHER = "other", "Other"

    class FloorStatus(models.TextChoices):

        ACTIVE = "active", "Active"
        INACTIVE = "inactive", "Inactive"
        UNDER_MAINTENANCE = "under_maintenance", "Under Maintenance"
        CLOSED = "closed", "Closed"

    building = models.ForeignKey(Building, on_delete=models.CASCADE, related_name="floors",)
    name = models.CharField(max_length=200,)
    slug = models.SlugField( max_length=200,)
    floor_number = models.IntegerField(default=0, help_text="0 = Ground Floor",)
    floor_type = models.CharField(max_length=30, choices=FloorType.choices, default=FloorType.GROUND,)
    description = models.TextField(blank=True,)
    status = models.CharField(max_length=30, choices=FloorStatus.choices, default=FloorStatus.ACTIVE,)
    sort_order = models.PositiveIntegerField(default=0,)
    metadata = models.JSONField(default=dict, blank=True,)

    class Meta:
        ordering = ["sort_order", "floor_number", "name",]

        constraints = [
            models.UniqueConstraint(
                fields=["building", "slug",],
                name="uq_floor_building_slug",
            ),

            models.UniqueConstraint(
                fields=["building", "floor_number",],
                name="uq_floor_building_number",
            ),
        ]

        indexes = [

            models.Index(
                fields=["building", "status",],
                name="idx_floor_building_status",
            ),

            models.Index(
                fields=["building", "sort_order",],
                name="idx_floor_building_order",
            ),
        ]

    def __str__(self):
        return (
            f"{self.building.name} - {self.name}"
        )


class RoomType(TimeStampedModel):
    """
    Sellable room category.
    """
    class RoomCategory(models.TextChoices):
        STANDARD = "standard", "Standard"
        DELUXE = "deluxe", "Deluxe"
        PREMIUM = "premium", "Premium"
        SUITE = "suite", "Suite"
        VILLA = "villa", "Villa"
        FAMILY = "family", "Family"
        DORMITORY = "dormitory", "Dormitory"
        OTHER = "other", "Other"

    class RoomTypeStatus(models.TextChoices):
        ACTIVE = "active", "Active"
        INACTIVE = "inactive", "Inactive"
        COMING_SOON = "coming_soon", "Coming Soon"

    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name="room_types",)
    name = models.CharField(max_length=200,)
    slug = models.SlugField(max_length=200,)
    code = models.CharField(max_length=30, blank=True,)
    category = models.CharField(max_length=30, choices=RoomCategory.choices, default=RoomCategory.STANDARD,)
    short_description = models.CharField(max_length=255, blank=True,)
    description = models.TextField(blank=True,)
    base_occupancy = models.PositiveSmallIntegerField(default=2,)
    max_occupancy = models.PositiveSmallIntegerField(default=2,)
    max_adults = models.PositiveSmallIntegerField(default=2,)
    max_children = models.PositiveSmallIntegerField(default=0,)
    room_size = models.DecimalField(max_digits=8, decimal_places=2, help_text="Area in square feet",)
    bed_configuration = models.CharField(max_length=100, blank=True,)
    status = models.CharField(max_length=30, choices=RoomTypeStatus.choices, default=RoomTypeStatus.ACTIVE,)
    sort_order = models.PositiveIntegerField(default=0,)
    metadata = models.JSONField(default=dict, blank=True,)

    class Meta:
        ordering = ["sort_order", "name",]

        constraints = [
            models.UniqueConstraint(
                fields=["property", "slug"],
                name="uq_roomtype_property_slug",
            ),
            models.UniqueConstraint(
                fields=["property", "name"],
                name="uq_roomtype_property_name",
            ),
        ]

        indexes = [
            models.Index(
                fields=["property", "status"],
                name="idx_roomtype_property_status",
            ),
            models.Index(
                fields=["property", "category"],
                name="idx_roomtype_property_category",
            ),
        ]

    def __str__(self):
        return f"{self.property.name} - {self.name}"


class RoomAmenity(TimeStampedModel):
    """
    Amenities available for a RoomType.
    """
    class AmenityCategory(models.TextChoices):
        BEDROOM = "bedroom", "Bedroom"
        BATHROOM = "bathroom", "Bathroom"
        ENTERTAINMENT = "entertainment", "Entertainment"
        INTERNET = "internet", "Internet"
        FOOD_BEVERAGE = "food_beverage", "Food & Beverage"
        COMFORT = "comfort", "Comfort"
        SAFETY = "safety", "Safety"
        ACCESSIBILITY = "accessibility", "Accessibility"
        OUTDOOR = "outdoor", "Outdoor"
        OTHER = "other", "Other"

    room_type = models.ForeignKey(RoomType, on_delete=models.CASCADE, related_name="amenities",)
    name = models.CharField(max_length=200,)
    slug = models.SlugField(max_length=200,)
    category = models.CharField(max_length=30, choices=AmenityCategory.choices, default=AmenityCategory.COMFORT,)
    description = models.TextField(blank=True,)
    icon = models.CharField(max_length=100, blank=True, help_text="Bootstrap or FontAwesome icon",)
    is_featured = models.BooleanField(default=False,)
    sort_order = models.PositiveIntegerField(default=0,)
    is_active = models.BooleanField(default=True,)
    metadata = models.JSONField(default=dict, blank=True,)

    class Meta:
        ordering = ["sort_order", "name",]

        constraints = [
            models.UniqueConstraint(
                fields=["room_type", "slug"],
                name="uq_roomamenity_roomtype_slug",
            ),
            models.UniqueConstraint(
                fields=["room_type", "name"],
                name="uq_roomamenity_roomtype_name",
            ),
        ]

        indexes = [
            models.Index(
                fields=["room_type", "category"],
                name="idx_roomamenity_category",
            ),
            models.Index(
                fields=["room_type", "is_active"],
                name="idx_roomamenity_active",
            ),
        ]

    def __str__(self):
        return f"{self.room_type.name} - {self.name}"


class Room(TimeStampedModel):
    """
    Individual physical room / inventory unit.
    """
    class RoomStatus(models.TextChoices):
        AVAILABLE = "available", "Available"
        OCCUPIED = "occupied", "Occupied"
        OUT_OF_ORDER = "out_of_order", "Out of Order"
        MAINTENANCE = "maintenance", "Maintenance"
        BLOCKED = "blocked", "Blocked"
        INACTIVE = "inactive", "Inactive"

    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name="rooms",)
    building = models.ForeignKey(Building, on_delete=models.SET_NULL, related_name="rooms", null=True, blank=True,)
    floor = models.ForeignKey(Floor, on_delete=models.SET_NULL, related_name="rooms", null=True, blank=True,)
    room_type = models.ForeignKey(RoomType, on_delete=models.PROTECT, related_name="rooms",)
    room_number = models.CharField(max_length=30,)
    room_name = models.CharField(max_length=200, blank=True,)
    slug = models.SlugField(max_length=200,)
    status = models.CharField(max_length=30, choices=RoomStatus.choices, default=RoomStatus.AVAILABLE,)
    max_adults = models.PositiveSmallIntegerField(default=2,)
    max_children = models.PositiveSmallIntegerField(default=2,)
    is_smoking = models.BooleanField(default=False,)
    is_accessible = models.BooleanField(default=False,)
    notes = models.TextField(blank=True,)
    sort_order = models.PositiveIntegerField(default=0,)
    metadata = models.JSONField(default=dict, blank=True,)

    class Meta:
        ordering = ["sort_order", "room_number",]

        constraints = [
            models.UniqueConstraint(
                fields=["property", "room_number"],
                name="uq_room_property_number",
            ),
            models.UniqueConstraint(
                fields=["property", "slug"],
                name="uq_room_property_slug",
            ),
        ]

        indexes = [
            models.Index(
                fields=["property", "status"],
                name="idx_room_property_status",
            ),
            models.Index(
                fields=["room_type", "status"],
                name="idx_room_roomtype_status",
            ),
            models.Index(
                fields=["building", "floor"],
                name="idx_room_building_floor",
            ),
        ]

    def __str__(self):
        return f"{self.property.name} - {self.room_number}"

class Guest(TimeStampedModel):
    """
    Customer staying at property.
    Independent from authentication users.
    """
    class Status(models.TextChoices):
        ACTIVE = "active", "Active"
        BLOCKED = "blocked", "Blocked"

    tenant = models.ForeignKey("tenants.Tenant", on_delete=models.CASCADE, related_name="guests",)
    first_name = models.CharField(max_length=100,)
    last_name = models.CharField(max_length=100, blank=True,)
    email = models.EmailField(blank=True,)
    phone = models.CharField(max_length=30, blank=True,)
    alternate_phone = models.CharField(max_length=30, blank=True,)
    date_of_birth = models.DateField(null=True, blank=True,)
    nationality = models.CharField(max_length=100, blank=True,)
    address = models.TextField(blank=True,)
    city = models.CharField(max_length=100, blank=True,)
    state = models.CharField(max_length=100, blank=True,)
    country = models.CharField(max_length=100, default="India",)
    id_type = models.CharField(max_length=50, blank=True,)
    id_number = models.CharField(max_length=100, blank=True,)
    preferences = models.JSONField(default=dict, blank=True, help_text="Guest preferences and history",)
    metadata = models.JSONField(default=dict, blank=True,)
    status = models.CharField( max_length=20, choices=Status.choices, default=Status.ACTIVE,)

    class Meta:
        ordering = ["first_name", "last_name",]

        constraints = [
            models.UniqueConstraint(
                fields=["tenant", "email",],
                name="uq_guest_tenant_email",
            ),
        ]
        indexes = [
            models.Index(
                fields=["tenant", "phone",],
                name="idx_guest_tenant_phone",
            ),
            models.Index(
                fields=["tenant", "email",],
                name="idx_guest_tenant_email",
            ),
        ]
        
    def __str__(self):
        return f"{self.first_name} {self.last_name}".strip()


class Reservation(TimeStampedModel):
    """
    Central booking transaction.
    """
    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        CONFIRMED = "confirmed", "Confirmed"
        CHECKED_IN = "checked_in", "Checked In"
        CHECKED_OUT = "checked_out", "Checked Out"
        CANCELLED = "cancelled", "Cancelled"
        NO_SHOW = "no_show", "No Show"

    class BookingSource(models.TextChoices):
        WEBSITE = "website", "Website"
        WALK_IN = "walk_in", "Walk In"
        PHONE = "phone", "Phone"
        OTA = "ota", "OTA"
        CORPORATE = "corporate", "Corporate"
        AGENT = "agent", "Travel Agent"

    class CancellationStatus(models.TextChoices):
        NOT_CANCELLED = "not_cancelled", "Not Cancelled"
        REQUESTED = "requested", "Requested"
        APPROVED = "approved", "Approved"
        REJECTED = "rejected", "Rejected"

    tenant = models.ForeignKey("tenants.Tenant", on_delete=models.CASCADE, related_name="reservations",)
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name="reservations",)
    guest = models.ForeignKey(Guest, on_delete=models.PROTECT, related_name="reservations",)
    booking_number = models.CharField(max_length=50, unique=True,)
    check_in = models.DateField()
    check_out = models.DateField()
    adults = models.PositiveIntegerField(default=1,)
    children = models.PositiveIntegerField(default=0,)
    booking_source = models.CharField(max_length=30,choices=BookingSource.choices, default=BookingSource.WEBSITE,)
    status = models.CharField( max_length=30, choices=Status.choices, default=Status.PENDING,)
    cancellation_status = models.CharField(max_length=30,choices=CancellationStatus.choices, default=CancellationStatus.NOT_CANCELLED,)
    cancellation_reason = models.TextField(blank=True,)
    total_amount = models.DecimalField(max_digits=12, decimal_places=2,default=0,)
    tax_amount = models.DecimalField(max_digits=12,decimal_places=2, default=0,)
    discount_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0,)
    paid_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0,)
    pricing_snapshot = models.JSONField( default=dict, blank=True,help_text="Frozen price details at booking time",)
    payment_summary = models.JSONField(default=dict,blank=True,)
    booking_metadata = models.JSONField(default=dict, blank=True,)

    class Meta:
        ordering = ["-created_at",]

        indexes = [
            models.Index(
                fields=["property", "check_in",],
                name="idx_reserv_prop_checkin",
            ),
            models.Index(
                fields=["guest",],
                name="idx_reserv_guest",
            ),
            models.Index(
                fields=["status",],
                name="idx_reserv_status",
            ),
        ]

    def __str__(self):
        return (
            f"{self.booking_number} - "
            f"{self.guest}"
        )


class ReservationRoom(TimeStampedModel):
    """
    Room-level reservation details.
    Connects Reservation with Room inventory.
    """
    class Status(models.TextChoices):
        RESERVED = "reserved", "Reserved"
        ASSIGNED = "assigned", "Assigned"
        CHECKED_IN = "checked_in", "Checked In"
        CHECKED_OUT = "checked_out", "Checked Out"
        CANCELLED = "cancelled", "Cancelled"

    reservation = models.ForeignKey(Reservation, on_delete=models.CASCADE, related_name="rooms",)
    room_type = models.ForeignKey(RoomType, on_delete=models.PROTECT, related_name="reservation_rooms",)
    room = models.ForeignKey(Room, on_delete=models.SET_NULL, null=True, blank=True, related_name="reservation_rooms", help_text="Actual assigned physical room",)
    rate_plan = models.ForeignKey("pricing.RatePlan", on_delete=models.PROTECT, related_name="reservation_rooms",)
    rooms_count = models.PositiveIntegerField(default=1,)
    adults = models.PositiveIntegerField(default=1,)
    children = models.PositiveIntegerField(default=0,)
    check_in = models.DateField()
    check_out = models.DateField()
    nightly_price_snapshot = models.JSONField(default=dict, blank=True, help_text="Frozen nightly pricing",)
    subtotal = models.DecimalField(max_digits=12, decimal_places=2, default=0,)
    discount_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0,)
    tax_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0,)
    final_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0,)
    status = models.CharField( max_length=30, choices=Status.choices, default=Status.RESERVED,)
    metadata = models.JSONField(default=dict, blank=True,)

    class Meta:
        ordering = ["created_at",]

        indexes = [
            models.Index(
                fields=["reservation",],
                name="idx_reserv_room_reservation",
            ),
            models.Index(
                fields=["room", "check_in","check_out",],
                name="idx_reserv_room_dates",
            ),
            models.Index(
                fields=["room_type",],
                name="idx_reserv_room_type",
            ),
        ]

    def __str__(self):
        return (
            f"{self.reservation.booking_number} - "
            f"{self.room_type.name}"
        )



class ReservationGuest(TimeStampedModel):
    """
    Individual guest attached to a reservation.
    """
    class GuestRole(models.TextChoices):
        PRIMARY = "primary", "Primary Guest"
        ADULT = "adult", "Adult"
        CHILD = "child", "Child"
        INFANT = "infant", "Infant"

    class IdentityStatus(models.TextChoices):
        PENDING = "pending", "Pending"
        VERIFIED = "verified", "Verified"
        REJECTED = "rejected", "Rejected"

    reservation = models.ForeignKey(Reservation, on_delete=models.CASCADE, related_name="reservation_guests",)
    reservation_room = models.ForeignKey(ReservationRoom, on_delete=models.CASCADE, related_name="guests", null=True, blank=True, help_text="Assigned room within reservation.",)
    guest = models.ForeignKey( Guest, on_delete=models.PROTECT, related_name="reservation_history",)
    role = models.CharField(max_length=20, choices=GuestRole.choices, default=GuestRole.ADULT,)
    is_primary = models.BooleanField(default=False,)
    identity_status = models.CharField(max_length=20, choices=IdentityStatus.choices, default=IdentityStatus.PENDING,)
    check_in_completed = models.BooleanField(default=False,)
    special_requests = models.TextField(blank=True,)
    metadata = models.JSONField(default=dict, blank=True,)
    
    class Meta:
        ordering = ["reservation", "-is_primary", "role", "guest",]

        constraints = [
            models.UniqueConstraint(
                fields=["reservation", "guest",],
                name="uq_reservation_guest",
            ),
        ]
        indexes = [
            models.Index(
                fields=["reservation", "role",],
                name="idx_res_guest_role",
            ),
            models.Index(
                fields=["reservation_room",],
                name="idx_res_guest_room",
            ),
            models.Index(
                fields=["guest",],
                name="idx_res_guest_guest",
            ),
        ]

    def __str__(self):
        guest_name = (f"{self.guest.first_name or ''} {self.guest.last_name or ''}").strip()

        if not guest_name:
            guest_name = self.guest.email or f"Guest #{self.guest.pk}"

        return f"{self.reservation.booking_number} - {guest_name}"


class ReservationPayment(TimeStampedModel):
    """
    Financial transactions linked with a reservation.
    """
    class PaymentType(models.TextChoices):
        PAYMENT = "payment", "Payment"
        REFUND = "refund", "Refund"
        ADJUSTMENT = "adjustment", "Adjustment"

    class PaymentMethod(models.TextChoices):
        CASH = "cash", "Cash"
        CARD = "card", "Card"
        UPI = "upi", "UPI"
        BANK_TRANSFER = "bank_transfer", "Bank Transfer"
        ONLINE = "online", "Online Gateway"
        OTHER = "other", "Other"

    class PaymentStatus(models.TextChoices):
        INITIATED = "initiated", "Initiated"
        PENDING = "pending", "Pending"
        SUCCESS = "success", "Success"
        FAILED = "failed", "Failed"
        REFUNDED = "refunded", "Refunded"
        CANCELLED = "cancelled", "Cancelled"

    reservation = models.ForeignKey(Reservation, on_delete=models.CASCADE, related_name="payments",)
    payment_type = models.CharField(max_length=20, choices=PaymentType.choices, default=PaymentType.PAYMENT,)
    payment_method = models.CharField(max_length=30, choices=PaymentMethod.choices, default=PaymentMethod.ONLINE,)
    status = models.CharField(max_length=20, choices=PaymentStatus.choices, default=PaymentStatus.PENDING,)
    amount = models.DecimalField(max_digits=12, decimal_places=2,)
    currency = models.CharField(max_length=10, default="INR",)
    gateway_name = models.CharField(max_length=100, blank=True,)
    gateway_transaction_id = models.CharField(max_length=200, blank=True,)
    gateway_order_id = models.CharField(max_length=200, blank=True,)
    paid_at = models.DateTimeField( null=True, blank=True,)
    failure_reason = models.TextField(blank=True,)
    metadata = models.JSONField(default=dict, blank=True,)

    class Meta:
        ordering = ["-created_at",]

        indexes = [
            models.Index(
                fields=["reservation", "status",],
                name="idx_res_payment_status",
            ),
            models.Index(
                fields=["gateway_transaction_id",],
                name="idx_payment_gateway_txn",
            ),
            models.Index(
                fields=["payment_method",],
                name="idx_payment_method",
            ),
        ]

    def __str__(self):
        return (
            f"{self.reservation.booking_number} "
            f"- {self.amount} {self.currency}"
        )


class ReservationStatusHistory(TimeStampedModel):
    """
    Immutable history of reservation status changes.
    """
    class ChangeSource(models.TextChoices):
        USER = "user", "User"
        SYSTEM = "system", "System"
        OTA = "ota", "OTA"
        PAYMENT = "payment", "Payment"
        AUTOMATION = "automation", "Automation"

    reservation = models.ForeignKey(Reservation, on_delete=models.CASCADE,  related_name="status_history",)
    previous_status = models.CharField(max_length=30, choices=Reservation.Status.choices, blank=True,)
    new_status = models.CharField(max_length=30, choices=Reservation.Status.choices,)
    changed_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name="reservation_status_changes",)
    change_source = models.CharField(max_length=20, choices=ChangeSource.choices, default=ChangeSource.USER,)
    reason = models.TextField(blank=True,)
    metadata = models.JSONField(default=dict, blank=True,)

    class Meta:
        ordering = ["-created_at",]

        indexes = [
            models.Index(
                fields=["reservation", "created_at",],
                name="idx_res_status_date",
            ),
            models.Index(
                fields=["new_status",],
                name="idx_res_new_status",
            ),
            models.Index(
                fields=["change_source",],
                name="idx_res_change_source",
            ),
        ]

    def __str__(self):
        return (
            f"{self.reservation.booking_number} : "
            f"{self.previous_status} → {self.new_status}"
        )