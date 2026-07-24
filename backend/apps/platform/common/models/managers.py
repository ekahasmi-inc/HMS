from django.db import models

from .querysets import BaseQuerySet


class BaseManager(models.Manager):
    """
    Default manager.
    """

    def get_queryset(self):
        return BaseQuerySet(
            self.model,
            using=self._db
        ).active()


class DeletedManager(models.Manager):
    """
    Manager for deleted records.
    """

    def get_queryset(self):
        return BaseQuerySet(
            self.model,
            using=self._db
        ).deleted()