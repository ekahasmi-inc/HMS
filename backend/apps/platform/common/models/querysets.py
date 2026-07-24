from django.db import models


class BaseQuerySet(models.QuerySet):
    """
    Base reusable queryset.
    """

    def active(self):
        """
        Return non-deleted records.
        """
        return self.filter(
            is_deleted=False
        )

    def deleted(self):
        """
        Return deleted records.
        """
        return self.filter(
            is_deleted=True
        )

    def hard_delete(self):
        """
        Permanently remove records.
        Use carefully.
        """
        return super().delete()