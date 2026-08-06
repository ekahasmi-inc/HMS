from django.contrib import admin
from .models import (
    Property,
    PropertyAmenity,
    Building,
    Floor,
    RoomType,
    RoomAmenity,
    Room,
    Guest,
    Reservation,
    ReservationRoom,
    ReservationGuest,
    ReservationPayment,
)

@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "tenant",
        "property_type",
        "status",
        "city",
        "country",
    )

    list_filter = (
        "property_type",
        "status",
        "country",
    )

    search_fields = (
        "name",
        "city",
        "state",
    )

    prepopulated_fields = {
        "slug": ("name",),
    }

    autocomplete_fields = (
        "tenant",
    )

@admin.register(PropertyAmenity)
class PropertyAmenityAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "property",
        "category",
        "is_featured",
        "is_active",
        "display_order",
    )

    list_filter = (
        "category",
        "is_active",
        "is_featured",
    )

    search_fields = (
        "name",
        "property__name",
    )

    autocomplete_fields = (
        "property",
    )

    prepopulated_fields = {
        "slug": ("name",),
    }

    ordering = (
        "property",
        "display_order",
        "name",
    )


@admin.register(Building)
class BuildingAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "property",
        "code",
        "total_floors",
        "status",
        "sort_order",
    )

    list_filter = (
        "status",
        "property",
    )

    search_fields = (
        "name",
        "code",
        "property__name",
    )

    ordering = (
        "property",
        "sort_order",
        "name",
    )

    prepopulated_fields = {
        "slug": ("name",),
    }

@admin.register(Floor)
class FloorAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "building",
        "floor_number",
        "floor_type",
        "status",
        "sort_order",
    )

    list_filter = (
        "status",
        "floor_type",
        "building",
    )

    search_fields = (
        "name",
        "building__name",
    )

    ordering = (
        "building",
        "sort_order",
        "floor_number",
    )

    prepopulated_fields = {
        "slug": ("name",)
    }

@admin.register(RoomType)
class RoomTypeAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "property",
        "category",
        "base_occupancy",
        "max_occupancy",
        "status",
        "sort_order",
    )

    list_filter = (
        "property",
        "category",
        "status",
    )

    search_fields = (
        "name",
        "code",
        "property__name",
    )

    ordering = (
        "property",
        "sort_order",
        "name",
    )

    prepopulated_fields = {
        "slug": ("name",)
    }


@admin.register(RoomAmenity)
class RoomAmenityAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "room_type",
        "category",
        "is_featured",
        "is_active",
        "sort_order",
    )

    list_filter = (
        "category",
        "is_featured",
        "is_active",
        "room_type__property",
    )

    search_fields = (
        "name",
        "room_type__name",
    )

    ordering = (
        "room_type",
        "sort_order",
        "name",
    )

    prepopulated_fields = {
        "slug": ("name",)
    }


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):

    list_display = (
        "room_number",
        "room_name",
        "property",
        "building",
        "floor",
        "room_type",
        "status",
    )

    list_filter = (
        "property",
        "building",
        "floor",
        "room_type",
        "status",
        "is_smoking",
        "is_accessible",
    )

    search_fields = (
        "room_number",
        "room_name",
    )

    ordering = (
        "property",
        "sort_order",
        "room_number",
    )

    prepopulated_fields = {
        "slug": ("room_number",)
    }


@admin.register(Guest)
class GuestAdmin(admin.ModelAdmin):

    list_display = (

        "first_name",
        "last_name",
        "phone",
        "email",
        "status",

    )


    list_filter = (

        "status",
        "country",

    )


    search_fields = (

        "first_name",
        "last_name",
        "phone",
        "email",

    )


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):

    list_display = (

        "booking_number",
        "guest",
        "property",
        "check_in",
        "check_out",
        "status",
        "total_amount",

    )


    list_filter = (

        "status",
        "booking_source",
        "property",

    )


    search_fields = (

        "booking_number",
        "guest__first_name",
        "guest__phone",
        "guest__email",

    )


    ordering = (

        "-created_at",

    )


@admin.register(ReservationRoom)
class ReservationRoomAdmin(admin.ModelAdmin):

    list_display = (

        "reservation",
        "room_type",
        "room",
        "rate_plan",
        "status",
        "final_amount",

    )


    list_filter = (

        "status",
        "room_type",

    )


    search_fields = (

        "reservation__booking_number",
        "room__room_number",
        "room_type__name",

    )



@admin.register(ReservationGuest)
class ReservationGuestAdmin(admin.ModelAdmin):

    list_display = (
        "reservation",
        "guest",
        "role",
        "reservation_room",
        "identity_status",
        "check_in_completed",
    )

    list_filter = (
        "role",
        "identity_status",
        "check_in_completed",
    )

    search_fields = (
        "reservation__booking_number",
        "guest__first_name",
        "guest__last_name",
        "guest__email",
        "guest__phone_number",
    )

    autocomplete_fields = (
        "reservation",
        "reservation_room",
        "guest",
    )


@admin.register(ReservationPayment)
class ReservationPaymentAdmin(admin.ModelAdmin):

    list_display = (

        "reservation",
        "payment_type",
        "payment_method",
        "amount",
        "status",
        "created_at",

    )


    list_filter = (

        "payment_type",
        "payment_method",
        "status",

    )


    search_fields = (

        "reservation__booking_number",
        "gateway_transaction_id",
        "gateway_order_id",

    )

    readonly_fields = (
        "created_at",
        "updated_at",

    )