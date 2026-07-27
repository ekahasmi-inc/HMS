from django.contrib import admin
from .models import Plan, Feature, Subscription

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

@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):

    list_display = ("tenant", "plan", "status", "billing_status", "start_date", "end_date",)
    list_filter = ("status", "billing_status", "auto_renew",)
    search_fields = ("tenant__name", "plan__name",)
    autocomplete_fields = ("tenant", "plan",)