from django.db import models
from .managers import BaseManager, DeletedManager

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

    objects = BaseManager()

    deleted_objects = DeletedManager()


    class Meta:
        abstract = True