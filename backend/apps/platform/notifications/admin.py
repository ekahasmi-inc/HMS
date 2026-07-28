from django.contrib import admin

from .models import NotificationTemplate


@admin.register(NotificationTemplate)
class NotificationTemplateAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "channel",
        "is_active",
    )

    list_filter = (
        "channel",
        "is_active",
    )

    search_fields = (
        "name",
        "code",
    )

    prepopulated_fields = {
        "code": ("name",)
    }