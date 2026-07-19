from django.urls import path

from .views import subscriber_view

app_name = "marketing"

urlpatterns = [
    path("subscriber/", subscriber_view, name="subscriber"),
]
