from uuid import uuid4

from django.conf import settings
from django.db import models
from django.utils import timezone


class UUIDMixin(models.Model):
    """
    Adds a UUID primary key.
    """

    id = models.UUIDField(
        primary_key=True,
        default=uuid4,
        editable=False,
    )

    class Meta:
        abstract = True


class TimestampMixin(models.Model):
    """
    Tracks creation and modification timestamps.
    """

    created_at = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        abstract = True


class AuditMixin(models.Model):
    """
    Tracks who created and last updated a record.
    """

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="%(class)s_created",
    )

    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="%(class)s_updated",
    )

    class Meta:
        abstract = True


class SoftDeleteMixin(models.Model):

    is_deleted = models.BooleanField(
        default=False,
        db_index=True,
    )

    deleted_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    deleted_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="%(class)s_deleted",
    )


    def delete(
        self,
        using=None,
        keep_parents=False
    ):
        """
        Soft delete.
        """

        self.is_deleted = True
        self.deleted_at = timezone.now()
        self.save(
            update_fields=[
                "is_deleted",
                "deleted_at",
            ]
        )


    def restore(self):
        """
        Restore deleted record.
        """

        self.is_deleted = False
        self.deleted_at = None

        self.save(
            update_fields=[
                "is_deleted",
                "deleted_at",
            ]
        )


    class Meta:
        abstract = True