from django.core.exceptions import ValidationError


def validate_file_size(
    file,
    max_size_mb=5
):
    """
    Generic file size validator.
    """

    max_size = (
        max_size_mb *
        1024 *
        1024
    )

    if file.size > max_size:
        raise ValidationError(
            "File size exceeded."
        )