from django.contrib import admin
from .models import (
    Property,
    PropertyAmenity,
    Building,
    Floor,
    RoomType,
    RoomAmenity,
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