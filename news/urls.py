from django.urls import path

from .views import pricing_view, subscriber_view

urlpatterns = [
    path("subscribe/", subscriber_view, name="subscribe"),
    path("pricing/", pricing_view, name="pricing"),
]
