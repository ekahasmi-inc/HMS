import re

from django.core.exceptions import ValidationError


def validate_phone_number(value):
    """
    Generic phone validation.
    """

    pattern = r"^\+?[0-9]{10,15}$"

    if not re.match(pattern, value):
        raise ValidationError(
            "Invalid phone number."
        )


def validate_positive(value):
    """
    Ensure number is positive.
    """

    if value < 0:
        raise ValidationError(
            "Value must be positive."
        )