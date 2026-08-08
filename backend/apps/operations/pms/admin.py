from django.contrib import admin

from .models import CheckIn, CheckOut

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
        "reservation__booking_number",
        "guest__first_name",
        "guest__last_name",
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