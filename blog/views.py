from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Prefetch
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from blog.forms import CommentCreateViewForm

from .models import Article, Category, Comment
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

    breadcrumbs = [{"title": "Home", "url": reverse("core:home")}, {"title": "Blogs"}]
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

    article = get_object_or_404(
        Article.objects.select_related("category_main").prefetch_related(
            Prefetch(
                "comments",
                queryset=Comment.objects.filter(status=Comment.Status.APPROVED),
            ),
            "tags",
        ),
        slug=slug,
    )
    context = {
        "meta_description": article.meta_description,
    }

    pagination = Paginator(article.comments.all(), 10)  # type: ignore
    page_comments = pagination.get_page(request.GET.get("page"))

    if request.method == "POST":
        form = CommentCreateViewForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.article = article
            comment.save()
            messages.success(
                request,
                """Your comment has been successfully submitted! We will display it after 
                review.""",
            )
            return redirect("blog:detail", slug=article.slug)
        else:
            pass
    else:
        form = CommentCreateViewForm()

    return render(
        request,
        "blog/blog_detail.html",
        {
            "article": article,
            "breadcrumbs": build_article_breadcrumb(article)
            if article.category_main
            else [],
            **context,
            "page_comments": page_comments,
            "form": form,
        },
    )
