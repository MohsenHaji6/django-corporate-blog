import csv
from io import StringIO

from django.contrib import admin
from django.test import RequestFactory, TestCase
from django.utils import timezone

from marketing.admin import SubscriberAdmin
from marketing.models import Subscriber


class SubscriberAdminTest(TestCase):
    def test_has_add_permission(self):
        admin_instance = SubscriberAdmin(Subscriber, admin.site)
        request = RequestFactory().get("/admin/")

        self.assertFalse(admin_instance.has_add_permission(request))

    def test_export_subscribers_csv(self):
        subscriber1 = Subscriber.objects.create(
            name="Test 1",
            phone_number="09121111111",
        )
        subscriber2 = Subscriber.objects.create(
            name="Test 2",
            phone_number="09122222222",
        )

        queryset = Subscriber.objects.all()
        request = RequestFactory().get("/admin/")

        admin_instance = SubscriberAdmin(Subscriber, admin.site)

        response = admin_instance.export_subscribers_csv(
            request,
            queryset,
        )

        self.assertEqual(
            response["Content-Type"],
            "text/csv; charset=utf-8",
        )

        self.assertEqual(
            response["Content-Disposition"],
            'attachment; filename="subscribers.csv"',
        )

        self.assertTrue(response.content.startswith(b"\xef\xbb\xbf"))

        content = response.content.decode("utf-8-sig")

        reader = csv.reader(StringIO(content))
        rows = list(reader)

        self.assertEqual(
            rows[0],
            ["Name", "Phone Number", "Created At"],
        )

        self.assertEqual(
            rows[1][0],
            subscriber1.name,
        )
        self.assertEqual(
            rows[1][1],
            '="09121111111"',
        )

        self.assertEqual(
            rows[2][0],
            subscriber2.name,
        )
        self.assertEqual(
            rows[2][1],
            '="09122222222"',
        )

    def test_export_subscribers_csv_formats_created_at(self):
        subscriber = Subscriber.objects.create(
            name="Test",
            phone_number="09121111111",
        )

        expected_date = timezone.localtime(subscriber.created_at).strftime(
            "%Y-%m-%d %H:%M"
        )

        request = RequestFactory().get("/admin/")
        admin_instance = SubscriberAdmin(Subscriber, admin.site)

        response = admin_instance.export_subscribers_csv(
            request,
            Subscriber.objects.filter(pk=subscriber.pk),
        )

        content = response.content.decode("utf-8-sig")
        reader = csv.reader(StringIO(content))
        rows = list(reader)

        self.assertEqual(rows[1][2], expected_date)
