from django.contrib import admin

from .models import CheckIn, CheckOut, RoomAssignment,RoomMove, GuestDocument,KeyCard

@admin.register(CheckIn)
class CheckInAdmin(admin.ModelAdmin):

    list_display = (
        "reservation",
        "guest",
        "property",
        "status",
        "actual_check_in",
    )


    list_filter = (
        "status",
        "property",
    )


    search_fields = (
        "document_number",
        "guest__name",
        "guest__email",
        "guest__phone",
    )


    readonly_fields = (
        "created_at",
        "updated_at",
    )

from .models import (
    CheckOut,
)


@admin.register(CheckOut)
class CheckOutAdmin(admin.ModelAdmin):

    list_display = (
        "reservation",
        "property",
        "status",
        "inspection_status",
        "actual_check_out",
    )


    list_filter = (
        "status",
        "inspection_status",
        "property",
    )


    search_fields = (
        "reservation__booking_number",
    )


    readonly_fields = (
        "created_at",
        "updated_at",
    )


@admin.register(RoomAssignment)
class RoomAssignmentAdmin(admin.ModelAdmin):

    list_display = (
        "reservation_room",
        "room",
        "status",
        "assignment_method",
        "change_type",
        "assigned_at",
        "effective_from",
        "effective_until",
    )

    list_filter = (
        "status",
        "assignment_method",
        "change_type",
    )

    search_fields = (
        "room__name",
        "room__room_number",
        "reservation_room__reservation__booking_number",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    autocomplete_fields = (
        "reservation_room",
        "room",
        "assigned_by",
    )

    ordering = (
        "-assigned_at",
        "-created_at",
    )


@admin.register(RoomMove)
class RoomMoveAdmin(admin.ModelAdmin):

    list_display = (
        "reservation",
        "reservation_room",
        "previous_room",
        "new_room",
        "status",
        "reason",
        "change_type",
        "initiated_by",
        "effective_at",
        "authorized_by",
    )

    list_filter = (
        "status",
        "reason",
        "change_type",
        "initiated_by",
    )

    search_fields = (
        "reservation__booking_number",
        "previous_room__name",
        "new_room__name",
        "notes",
    )

    autocomplete_fields = (
        "reservation",
        "reservation_room",
        "previous_assignment",
        "new_assignment",
        "previous_room",
        "new_room",
        "authorized_by",
    )

    readonly_fields = (
        "requested_at",
        "completed_at",
        "created_at",
        "updated_at",
    )

    ordering = (
        "-effective_at",
        "-created_at",
    )


@admin.register(GuestDocument)
class GuestDocumentAdmin(admin.ModelAdmin):

    list_display = (
        "guest",
        "document_type",
        "document_number",
        "issuing_country",
        "verification_status",
        "expiry_date",
        "verified_at",
        "verified_by",
    )

    list_filter = (
        "document_type",
        "verification_status",
        "issuing_country",
    )

    search_fields = (
        "document_number",
        "guest__first_name",
        "guest__last_name",
        "guest__email",
        "guest__phone",
    )

    autocomplete_fields = (
        "guest",
        "verified_by",
        "media_reference",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    ordering = (
        "-created_at",
    )



@admin.register(KeyCard)
class KeyCardAdmin(admin.ModelAdmin):

    list_display = (
        "credential_number",
        "card_type",
        "guest",
        "reservation",
        "room",
        "status",
        "issued_at",
        "expires_at",
        "issued_by",
    )

    list_filter = (
        "card_type",
        "status",
    )

    search_fields = (
        "credential_number",
        "guest__name",
        "guest__email",
        "reservation__booking_number",
        "room__name",
    )

    autocomplete_fields = (
        "reservation",
        "guest",
        "check_in",
        "room",
        "issued_by",
        "returned_by",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    ordering = (
        "-issued_at",
        "-created_at",
    )