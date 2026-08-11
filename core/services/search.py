from django.core.paginator import Paginator
from django.db.models import Case, Exists, IntegerField, OuterRef, Q, Value, When

from blog.models import Article, Tag


def search(query, request):
    if not query or len(query) < 3:
        return []

    query = query.split()
    query = set([word for word in query if len(word) >= 3])

    title = content = tag = category = Q()

    for word in query:
        title |= Q(title__icontains=word)
        content |= Q(content__icontains=word)
        category |= Q(category_main__name__icontains=word)
        tag |= Q(name__icontains=word)

    tags_exists = Tag.objects.filter(articles=OuterRef("pk")).filter(tag)

    articles = (
        Article.objects.filter(status=Article.Status.PUBLISHED)
        .annotate(has_tag=Exists(tags_exists))
        .annotate(
            search_score=(
                Case(
                    When(title, then=Value(10)),
                    default=Value(0),
                    output_field=IntegerField(),
                )
                + Case(
                    When(content, then=Value(5)),
                    default=Value(0),
                    output_field=IntegerField(),
                )
                + Case(
                    When(has_tag=True, then=Value(3)),
                    default=Value(0),
                    output_field=IntegerField(),
                )
                + Case(
                    When(category, then=Value(2)),
                    default=Value(0),
                    output_field=IntegerField(),
                )
            )
        )
        .filter(search_score__gt=0)
        .select_related("category_main")
        .order_by("-search_score")
    )

    pagination = Paginator(articles, 15)
    page_results = pagination.get_page(request.GET.get("page"))

    return page_results
