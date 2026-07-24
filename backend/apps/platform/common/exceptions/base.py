class ApplicationError(Exception):
    """
    Base exception for application errors.
    """

    default_message = "Application error occurred."

    def __init__(self, message=None):
        self.message = (
            message
            or self.default_message
        )

        super().__init__(self.message)


class ValidationError(ApplicationError):
    """
    Business validation failure.
    """

    default_message = "Validation failed."


class BusinessRuleError(ApplicationError):
    """
    Business rule violation.
    """

    default_message = "Business rule violation."


class PermissionDenied(ApplicationError):
    """
    Permission failure.
    """

    default_message = "Permission denied."


class ConfigurationError(ApplicationError):
    """
    Configuration problem.
    """

    default_message = "Invalid configuration."


class IntegrationError(ApplicationError):
    """
    External service failure.
    """

    default_message = "Integration failed."