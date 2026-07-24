from .base import ApplicationError


class APIError(ApplicationError):
    """
    API layer exception.
    """

    status_code = 400


class AuthenticationError(APIError):

    status_code = 401


class NotFoundError(APIError):

    status_code = 404