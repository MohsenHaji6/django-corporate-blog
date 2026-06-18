from django.core.exceptions import ValidationError


def validate_phone_number(phone_number):

    if not (
        phone_number.isdigit()
        and len(phone_number) == 11
        and phone_number.startswith("09")
    ):
        raise ValidationError("Phone number is invalid.")
