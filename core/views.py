from django.shortcuts import render
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from .services.search import search


def home_view(request):
    return render(request, "core/home.html")


def about_view(request):
    breadcrumbs = [
        {
            "title": _("Home"),
            "url": reverse("home"),
        },
        {
            "title": _("About"),
        },
    ]
    return render(request, "core/about.html", {"breadcrumbs": breadcrumbs})


def contact_view(request):
    breadcrumbs = [
        {
            "title": _("Home"),
            "url": reverse("home"),
        },
        {
            "title": _("Contact"),
        },
    ]
    return render(request, "core/contact.html", {"breadcrumbs": breadcrumbs})


def search_view(request):
    # Perform search logic here
    query = request.GET.get("q", "")
    # ... (search logic)
    blogs = search(query)

    return render(request, "core/search.html", {"blogs": blogs, "query": query})
