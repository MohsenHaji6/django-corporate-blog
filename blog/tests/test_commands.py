from datetime import timedelta

from django.core.management import call_command
from django.utils import timezone

from blog.models import Article
from blog.tests.base import BaseBlogTest


class PublishScheduledArticlesTest(BaseBlogTest):
    def test_just_change_scheduled_article_to_published_article(self):
        for i, status in enumerate(
            [
                Article.Status.SCHEDULED,
                Article.Status.DRAFT,
                Article.Status.ARCHIVED,
                Article.Status.PUBLISHED,
            ]
        ):
            self.create_article(
                title=f"test {i}",
                status=status,
            )

        call_command("publish_scheduled_articles")

        articles = Article.objects.filter(status=Article.Status.PUBLISHED).count()

        self.assertEqual(articles, 2)

    def test_publishes_only_scheduled_articles_due_now(self):

        for i, status in enumerate(
            [
                Article.Status.SCHEDULED,
                Article.Status.SCHEDULED,
            ]
        ):
            if i == 0:
                self.create_article(
                    title=f"test {i}",
                    status=status,
                    published_at=timezone.now() + timedelta(minutes=1),
                )
            else:
                self.create_article(
                    title=f"test {i}",
                    status=status,
                    published_at=timezone.now() - timedelta(minutes=1),
                )

        call_command("publish_scheduled_articles")

        published_article_count = Article.objects.filter(
            status=Article.Status.PUBLISHED
        ).count()

        self.assertEqual(published_article_count, 1)
