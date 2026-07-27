from django.contrib import admin
from .models import Plan, Feature

@admin.register(Plan)
class PlanAdmin(admin.ModelAdmin):
    list_display = ("name", "billing_cycle", "price", "currency", "is_active",)
    search_fields = ("name", "code",)
    list_filter = ("billing_cycle", "is_active",)

    prepopulated_fields = {
        "code": ("name",)
    }

@admin.register(Feature)
class FeatureAdmin(admin.ModelAdmin):
    list_display = ("name","category","code","is_active","display_order",)
    list_filter = ("category", "is_active",)
    search_fields = ("name", "code",)
    prepopulated_fields = {
        "code": ("name",)
    }

    ordering = ( "category","display_order", "name",)