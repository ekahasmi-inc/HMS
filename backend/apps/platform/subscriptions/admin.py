from django.contrib import admin
from .models import Plan

@admin.register(Plan)
class PlanAdmin(admin.ModelAdmin):
    list_display = ("name", "billing_cycle", "price", "currency", "is_active",)
    search_fields = ("name", "code",)
    list_filter = ("billing_cycle", "is_active",)

    prepopulated_fields = {
        "code": ("name",)
    }