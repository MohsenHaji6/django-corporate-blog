from django.contrib import messages
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from .forms import ContactMessageForm
from .services.search import search

# from blog.models import Article


def home_view(request):
    # latest_articles = Article.objects.filter(datetime_published=)
    return render(request, "core/home.html")


def about_view(request):
    breadcrumbs = [
        {
            "title": _("Home"),
            "url": reverse("core:home"),
        },
        {
            "title": _("About"),
        },
    ]
    return render(request, "core/about.html", {"breadcrumbs": breadcrumbs})


def contact_view(request):

    if request.method == "POST":
        form = ContactMessageForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, """Your message has been sent successfully!""")
            return redirect("core:contact")
        else:
            pass
    else:
        form = ContactMessageForm()

    breadcrumbs = [
        {
            "title": _("Home"),
            "url": reverse("core:home"),
        },
        {
            "title": _("Contact"),
        },
    ]
    return render(request, "core/contact.html", {"breadcrumbs": breadcrumbs, "form": form})


def search_view(request):
    # Perform search logic here
    query = request.GET.get("q", "")
    # ... (search logic)
    blogs = search(query)

    return render(request, "core/search.html", {"blogs": blogs, "query": query})
