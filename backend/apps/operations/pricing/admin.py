from django.contrib import admin
from .models import RatePlan, RateRule,Season

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


@admin.register(RateRule)
class RateRuleAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "rate_plan",
        "rule_type",
        "adjustment_value",
        "priority",
        "status",
    )

    list_filter = (
        "rule_type",
        "status",
    )

    search_fields = (
        "name",
        "rate_plan__name",
        "property__name",
    )

    ordering = (
        "priority",
        "name",
    )



@admin.register(Season)
class SeasonAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "property",
        "season_type",
        "start_date",
        "end_date",
        "status",
        "priority",
    )


    list_filter = (
        "season_type",
        "status",
    )


    search_fields = (
        "name",
        "property__name",
    )


    ordering = (
        "priority",
        "start_date",
    )