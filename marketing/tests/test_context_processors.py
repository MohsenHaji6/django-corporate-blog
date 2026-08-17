from django.test import TestCase
from django.urls import reverse


class SubscriberFormTest(TestCase):
    def test_redirects_subscriber_form_empty(self):
        response = self.client.get(reverse("core:home"))
        subscriber_form = response.context["subscriber_form"]

        self.assertFalse(subscriber_form.is_bound)