from django.contrib import admin
from .models import RatePlan, RateRule,Season, PriceCalendar, DerivedRate

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


@admin.register(PriceCalendar)
class PriceCalendarAdmin(admin.ModelAdmin):

    list_display = (

        "date",
        "property",
        "room_type",
        "rate_plan",
        "final_price",
        "channel",
        "status",

    )


    list_filter = (

        "property",
        "channel",
        "status",
        "date",

    )


    search_fields = (

        "room_type__name",
        "rate_plan__name",

    )


    ordering = (
        "date",

    )


@admin.register(DerivedRate)
class DerivedRateAdmin(admin.ModelAdmin):

    list_display = (

        "name",
        "parent_rate_plan",
        "adjustment_type",
        "adjustment_value",
        "channel",
        "status",

    )


    list_filter = (

        "status",
        "adjustment_type",
        "channel",

    )


    search_fields = (

        "name",
        "parent_rate_plan__name",

    )


    ordering = (

        "priority",
        "name",

    )