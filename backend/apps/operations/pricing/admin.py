from django.contrib import admin
from .models import RatePlan


@admin.register(RatePlan)
class RatePlanAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "property",
        "rate_type",
        "status",
        "is_refundable",
        "includes_breakfast",
    )

    list_filter = (
        "status",
        "rate_type",
    )

    search_fields = (
        "name",
        "property__name",
        "code",
    )

    filter_horizontal = (
        "room_types",
    )

    ordering = (
        "property",
        "name",
    )