from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Prefetch
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from blog.forms import CommentForm
from core.services import (
    build_article_breadcrumb,
    build_category_breadcrumb,
    build_category_tree,
)

from .models import Article, Category, Comment, Tag


def blog_list_view(request):

    articles = (
        Article.objects.select_related("category_main")
        .filter(status=Article.Status.PUBLISHED)
        .only(
            "pk",
            "title",
            "summary",
            "updated_at",
            "category_main",
            "slug",
            "image",
            "image_alt_text",
        )
    )

    pagination = Paginator(articles, 15)
    page_articles = pagination.get_page(request.GET.get("page"))

    breadcrumbs = [{"title": "Home", "url": reverse("core:home")}, {"title": "Blog"}]
    return render(
        request,
        "blog/blog_list.html",
        {
            "articles": page_articles,
            "categories": build_category_tree(),
            "breadcrumbs": breadcrumbs,
        },
    )


def blog_category_list_view(request, slug):
    category = get_object_or_404(Category, slug=slug)
    articles = Article.objects.filter(
        status=Article.Status.PUBLISHED, category_main=category
    )

    pagination = Paginator(articles, 15)
    page_articles = pagination.get_page(request.GET.get("page"))

    open_category_ids = [
        cat.id  # type: ignore
        for cat in category.get_ancestors()
    ]
    open_category_ids.append(category.id)  # type: ignore

    print(open_category_ids)
    return render(
        request,
        "blog/blog_list.html",
        {
            "articles": page_articles,
            "categories": build_category_tree(),
            "category": category,
            "open_category_ids": open_category_ids,
            "breadcrumbs": build_category_breadcrumb(category),
        },
    )


def blog_tag_list_view(request, slug):
    tag = get_object_or_404(Tag, slug=slug)

    articles = Article.objects.filter(
        status=Article.Status.PUBLISHED, tags=tag
    ).select_related("category_main")

    pagination = Paginator(articles, 15)
    page_articles = pagination.get_page(request.GET.get("page"))

    categories = Category.objects.filter(
        id__in=articles.values_list("category_main_id", flat=True).distinct()
    )

    paths = set()
    for category in categories:
        p = category.path
        while True:
            paths.add(p)

            if len(p) == Category.steplen:
                break

            p = p[: -Category.steplen]

    tags = Tag.objects.all()

    breadcrumbs = [
        {"title": "Home", "url": reverse("core:home")},
        {"title": "Blog", "url": reverse("blog:list")},
        {"title": tag},
    ]

    return render(
        request,
        "blog/blog_list.html",
        {
            "articles": page_articles,
            "breadcrumbs": breadcrumbs,
            "categories": build_category_tree(paths),
            "tag": tag,
            "tags": tags,
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
        form = CommentForm(request.POST)
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
        form = CommentForm()

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
