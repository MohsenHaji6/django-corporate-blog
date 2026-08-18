from django.core.exceptions import ValidationError
from django.test import TestCase

from accounts.validators import validate_phone_number


class ValidatePhoneNumberTest(TestCase):
    def subTest(self, phone_number):
        with self.assertRaises(ValidationError) as context:
            validate_phone_number(phone_number)
        self.assertEqual(context.exception.messages, ["Phone number is invalid."])

    def test_phone_number_is_not_digit(self):
        self.subTest(phone_number="0912111111a")

    def test_phone_number_len_not_equal_with_11(self):
        self.subTest(phone_number="091211111111")

    def test_phone_number_starts_not_with_09(self):
        self.subTest(phone_number="98912111111")

    def test_valid_phone_number(self):
        phone_number = "09121111111"

        try:
            validate_phone_number(phone_number)
        except ValidationError:
            self.fail("validate_phone_number() raised ValidationError unexpectedly.")
