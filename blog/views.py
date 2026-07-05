from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, render

from .models import Article, Category
from .services.breadcrumb import build_article_breadcrumb, build_category_breadcrumb
from .services.category_tree import build_category_tree


def blog_list_view(request):

    articles = (
        Article.objects.select_related("category_main")
        .filter(status=Article.Status.PUBLISHED)
        .only(
            "pk",
            "title",
            "summary",
            "datetime_updated",
            "category_main",
            "slug",
            "image",
            "image_alt_text",
        )
    )

    pagination = Paginator(articles, 15)
    page_articles = pagination.get_page(request.GET.get("page"))

    breadcrumbs = [{"title": "Home", "url": "/"}, {"title": "Blogs"}]
    return render(
        request,
        "blog/blog_list.html",
        {
            "page_articles": page_articles,
            "categories": build_category_tree(),
            "breadcrumbs": breadcrumbs,
        },
    )


def category_list_view(request, slug):
    category = get_object_or_404(Category, slug=slug)
    articles = Article.objects.filter(
        status=Article.Status.PUBLISHED, category_main=category
    )
    return render(
        request,
        "blog/blog_list.html",
        {
            "articles": articles,
            "categories": build_category_tree(),
            "breadcrumbs": build_category_breadcrumb(category),
        },
    )


def blog_detail_view(request, slug):

    article = get_object_or_404(Article, slug=slug)
    context = {
        "meta_description": article.meta_description,
    }
    return render(
        request,
        "blog/blog_detail.html",
        {
            "article": article,
            "breadcrumbs": build_article_breadcrumb(article)
            if article.category_main
            else [],
            **context,
        },
    )
