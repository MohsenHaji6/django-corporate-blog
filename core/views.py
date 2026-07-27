from django.contrib import messages
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from blog.models import Article, Category
from catalog.models import ProductVariant

from .forms import ContactMessageForm
from .models import Address, Page, PhoneNumber, SocialLink
from .services import search


def home_view(request):
    root_categories = Category.get_root_nodes()
    page = (
        Page.objects.filter(page_type=Page.PageType.CONTACT)
        .only("short_description")
        .first()
    )
    articles = Article.objects.filter(status=Article.Status.PUBLISHED).select_related(
        "category_main"
    )[:3]
    products = ProductVariant.objects.filter(in_stock=True).order_by("-updated_at")[:4]

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
        {
            "articles": articles,
            "products": products,
            "contact_form": form,
            "page": page,
            "root_categories": root_categories,
        },
    )


def about_view(request):
    page = Page.objects.filter(page_type=Page.PageType.ABOUT).first()
    breadcrumbs = [
        {
            "title": _("Home"),
            "url": reverse("core:home"),
        },
        {
            "title": _("About"),
        },
    ]
    return render(request, "core/about.html", {"breadcrumbs": breadcrumbs, "page": page})


def contact_view(request):
    phones = PhoneNumber.objects.filter(is_active=True).order_by("display_order")
    addresses = Address.objects.filter(is_active=True).order_by("display_order")
    social_links = SocialLink.objects.all().order_by("display_order")
    page = Page.objects.filter(page_type=Page.PageType.CONTACT).first()

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
    return render(
        request,
        "core/contact.html",
        {
            "breadcrumbs": breadcrumbs,
            "form": form,
            "phones": phones,
            "addresses": addresses,
            "social_links": social_links,
            "page": page,
        },
    )


def search_view(request):
    # Perform search logic here
    query = request.GET.get("q", "")
    # ... (search logic)
    articles = search(query, request)

    return render(request, "core/search.html", {"articles": articles, "query": query})


def privacy_view(request):
    page = Page.objects.filter(page_type=Page.PageType.PRIVACY).first()

    breadcrumbs = [
        {
            "title": _("Home"),
            "url": reverse("core:home"),
        },
        {
            "title": _("Privacy Policy"),
        },
    ]
    return render(request, "core/privacy.html", {"breadcrumbs": breadcrumbs, "page": page})
