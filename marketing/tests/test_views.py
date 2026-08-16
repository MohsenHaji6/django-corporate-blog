from django.test import TestCase
from django.urls import reverse

from marketing.models import Subscriber


class SubscriberViewTest(TestCase):
    def test_subscriber_form_save_in_database(self):
        self.client.post(
            reverse("marketing:subscriber"),
            data={"name": "Test", "phone_number": "09121111111"},
        )
        subscriber = Subscriber.objects.get()
        self.assertEqual(subscriber.name, "Test")
        self.assertEqual(subscriber.phone_number, "09121111111")

    def test_valid_subscriber_form_return_as_json(self):
        response = self.client.post(
            reverse("marketing:subscriber"),
            data={"name": "Test", "phone_number": "09121111111"},
        )

        data = response.json()
        self.assertTrue(data["success"])
        self.assertEqual(data["message"], "Subscription successful.")

    def test_invalid_subscriber_form_returns_errors(self):
        response = self.client.post(
            reverse("marketing:subscriber"),
            data={},
        )

        data = response.json()
        self.assertFalse(data["success"])
        self.assertIn("name", data["errors"])
        self.assertIn("phone_number", data["errors"])
        self.assertEqual(response.status_code, 400)

    def test_invalid_method_subscriber_form(self):
        response = self.client.get(
            reverse("marketing:subscriber"),
            data={"name": "Test", "phone_number": "09121111111"},
        )

        data = response.json()
        self.assertEqual(response.status_code, 405)
        self.assertFalse(data["success"])
        self.assertEqual(data["message"], "Invalid request method.")
