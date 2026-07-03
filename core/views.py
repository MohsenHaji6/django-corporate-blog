from django.db.models import Q
from django.shortcuts import render
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from blog.models import Article


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
    query = request.GET.get("q")
    # ... (search logic)
    blogs = (
        Article.objects.filter(
            Q(title__icontains=query)
            | Q(content__icontains=query)
            | Q(tags__name__icontains=query)
            | Q(category_main__name__icontains=query)
        ).distinct()
        if query
        else []
    )
    return render(request, "core/search.html", {"blogs": blogs, "query": query})
