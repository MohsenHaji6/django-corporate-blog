import csv

from django.contrib import admin
from django.http import HttpRequest, HttpResponse
from django.utils import timezone

from .models import Subscriber


@admin.register(Subscriber)
class SubscriberAdmin(admin.ModelAdmin):
    list_display = ["name", "phone_number", "created_at"]
    search_fields = ["name", "phone_number"]
    list_filter = ["created_at"]
    actions = ["export_subscribers_csv"]

    def has_add_permission(self, request: HttpRequest) -> bool:
        return False

    @admin.action(description="Export selected subscribers to CSV")
    def export_subscribers_csv(self, request, queryset):
        response = HttpResponse(content_type="text/csv; charset=utf-8")
        response["Content-Disposition"] = 'attachment; filename="subscribers.csv"'

        # To display Persian correctly in Excel
        response.write("\ufeff")

        writer = csv.writer(response)
        writer.writerow(["Name", "Phone Number", "Created At"])

        for subscriber in queryset:
            writer.writerow(
                [
                    subscriber.name,
                    f'="{subscriber.phone_number}"',
                    timezone.localtime(subscriber.created_at).strftime("%Y-%m-%d %H:%M"),
                ]
            )

        return response
