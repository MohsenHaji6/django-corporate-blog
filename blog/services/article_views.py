from datetime import date

from django.db.models import F

from blog.models import Article, ArticleView


def register_article_view(request, article):

    if not request.session.session_key:
        request.session.create()

    session_key = request.session.session_key

    _, created = ArticleView.objects.get_or_create(
        article=article, session_key=session_key, viewed_date=date.today()
    )

    if created:
        Article.objects.filter(pk=article.pk).update(views_count=F("views_count") + 1)
