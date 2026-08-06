from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from blog.models import Article, Category, Tag
from core.models.site_setting import SiteSetting


class BaseBlogTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.category = Category.add_root(name="test category")
        cls.tag = Tag.objects.create(name="test tag")
        cls.user = get_user_model().objects.create_user(phone_number="09123456789")  # type: ignore
        SiteSetting.objects.create(
            site_title="test site title",
            site_description="test site description",
            meta_title="test meta title",
            meta_description="test meta description",
            hero_title="test hero title",
            hero_text="test hero text",
            hero_image="test-hero-image.jpg",
            logo="test-logo.jpg",
            favicon="test-favicon.jpg",
            email="test@mail.com",
        )

    def create_article(
        self,
        title="test article",
        status=Article.Status.PUBLISHED,
        category_main=None,
        tags=None,
    ):
        article = Article.objects.create(
            title=title,
            content="test content article",
            author=self.user,
            image="test.jpg",
            image_alt_text="test",
            category_main=category_main if category_main else self.category,
            status=status,
        )
        article.tags.set([tags if tags else self.tag])

        return article

    def get_article_url(self, slug=None):
        return reverse(
            "blog:detail", kwargs={"slug": slug if slug else self.create_article().slug}
        )

    def get_category_url(self, slug=None):
        return reverse(
            "blog:category", kwargs={"slug": slug if slug else self.category.slug}
        )

    def get_tag_url(self, slug=None):
        return reverse("blog:tag", kwargs={"slug": slug if slug else self.tag.slug})
