from rest_framework.permissions import BasePermission


class IsAuthenticatedUser(
    BasePermission
):
    """
    Basic authenticated user check.
    """

    def has_permission(
        self,
        request,
        view
    ):
        return (
            request.user
            and request.user.is_authenticated
        )


class IsAdminUser(
    BasePermission
):
    """
    Basic admin check.
    """

    def has_permission(
        self,
        request,
        view
    ):
        return (
            request.user
            and request.user.is_staff
        )