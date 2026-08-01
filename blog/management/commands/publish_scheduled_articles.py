from django.core.management.base import BaseCommand
from django.utils import timezone

from blog.models import Article


class Command(BaseCommand):
    help = "Publish scheduled articles"

    def handle(self, *args, **options):

        Article.objects.filter(
            status=Article.Status.SCHEDULED,
            published_at__lte=timezone.now(),
        ).update(status=Article.Status.PUBLISHED)
