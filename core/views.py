from django.shortcuts import render
from django.urls import reverse


def home_view(request):
    return render(request, "core/home.html")


def about_view(request):
    breadcrumbs = [
        {
            "title": "Home",
            "url": reverse("home"),
        },
        {
            "title": "About",
        },
    ]
    return render(request, "core/about.html", {"breadcrumbs": breadcrumbs})


def contact_view(request):
    breadcrumbs = [
        {
            "title": "Home",
            "url": reverse("home"),
        },
        {
            "title": "Contact",
        },
    ]
    return render(request, "core/contact.html", {"breadcrumbs": breadcrumbs})
