from django.db import models

from .mixins import (
    AuditMixin,
    SoftDeleteMixin,
    TimestampMixin,
    UUIDMixin,
)


class BaseModel(
    UUIDMixin,
    TimestampMixin,
    AuditMixin,
    SoftDeleteMixin,
):
    """
    Base class for all models.
    """

    class Meta:
        abstract = True