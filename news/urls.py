from django.urls import path

from .views import price_list_view, subscriber_view

urlpatterns = [
    path("subscribe/", subscriber_view, name="subscribe"),
    path("price-list/", price_list_view, name="price_list"),
]
