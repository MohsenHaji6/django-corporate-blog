from django.urls import path

from .views import about_view, contact_view, home_view, privacy_view, search_view

app_name = "core"

urlpatterns = [
    path("", home_view, name="home"),
    path("about/", about_view, name="about"),
    path("contact/", contact_view, name="contact"),
    path("search/", search_view, name="search"),
    path("privacy-policy/", privacy_view, name="privacy"),
]
