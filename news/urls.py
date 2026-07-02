from django.urls import path

from .views import subscriber_view

urlpatterns = [
    path("subscribe/", subscriber_view, name="subscribe"),
]
