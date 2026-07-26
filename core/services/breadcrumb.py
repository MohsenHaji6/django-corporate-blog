from django.urls import reverse


def build_category_breadcrumb(category, categories=[]):
    """
    Build a breadcrumb trail for a given category.

    Args:
        category (Category): The category for which to build the breadcrumb trail.

    Returns:
        list: A list of dictionaries representing the breadcrumb trail.
              Each dictionary contains 'title' and 'url' keys.
    """
    breadcrumbs = [
        {
            "title": "Home",
            "url": reverse("core:home"),
        },
        {
            "title": "Blog",
            "url": reverse("blog:list"),
        },
    ]

    for cat in categories:
        breadcrumbs.append(
            {
                "title": cat.name.capitalize(),
                "url": reverse("blog:category", kwargs={"slug": cat.slug}),
            }
        )

    breadcrumbs.append(
        {
            "title": category.name.capitalize(),
        }
    )
    return breadcrumbs


def build_article_breadcrumb(article):
    """
    Build a breadcrumb trail for a given article.

    Args:
        article (Article): The article for which to build the breadcrumb trail.

    Returns:
        list: A list of dictionaries representing the breadcrumb trail.
              Each dictionary contains 'title' and 'url' keys.
    """
    breadcrumbs = []
    if article.category_main:
        breadcrumbs.extend(build_category_breadcrumb(article.category_main))
        breadcrumbs[-1]["url"] = reverse(
            "blog:category", kwargs={"slug": article.category_main.slug}
        )
    breadcrumbs.append({"title": article.title})
    return breadcrumbs
