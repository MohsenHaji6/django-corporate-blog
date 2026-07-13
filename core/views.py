from django.contrib import messages
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from blog.models import Article
from news.models import ProductVariant

from .forms import ContactMessageForm
from .services.search import search


def home_view(request):

    articles = Article.objects.filter(status=Article.Status.PUBLISHED).select_related(
        "category_main"
    )[:3]
    products = ProductVariant.objects.filter(in_stock=True).order_by("-updated_date")[:3]

    if request.method == "POST":
        form = ContactMessageForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, """Your message has been sent successfully!""")
            return redirect("core:home")
        else:
            pass
    else:
        form = ContactMessageForm()

    return render(
        request,
        "core/home.html",
        {"articles": articles, "products": products, "contact_form": form},
    )


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
    articles = search(query)

    return render(request, "core/search.html", {"articles": articles, "query": query})
