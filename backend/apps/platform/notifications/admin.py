from django.contrib import admin
from .models import NotificationTemplate, Notification


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

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):

    list_display = (
        "template",
        "tenant",
        "status",
        "recipient_email",
        "created_at",
    )

    list_filter = (
        "status",
        "template__channel",
    )

    search_fields = (
        "recipient_email",
        "recipient_phone",
        "subject",
    )

    autocomplete_fields = (
        "tenant",
        "template",
        "recipient",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )