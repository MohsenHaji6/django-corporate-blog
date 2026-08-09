from unittest.mock import Mock, patch

from django.contrib import admin, messages

from blog.admin import ArticleAdmin, CategoryAdmin, CommentAdmin, TagAdmin
from blog.forms import ArticleAdminForm
from blog.models import Article, Category, Comment, Tag

from .base import BaseBlogTest


class CategoryAdminTest(BaseBlogTest):
    def test_published_article_count_for_categories(self):

        for i, status in enumerate(
            [
                Article.Status.DRAFT,
                Article.Status.PUBLISHED,
                Article.Status.PUBLISHED,
                Article.Status.SCHEDULED,
                Article.Status.ARCHIVED,
            ]
        ):
            self.create_article(title=f"test {i}", status=status)

        request = self.get_admin_request()
        admin_instance = CategoryAdmin(Category, admin.site)

        queryset = admin_instance.get_queryset(request)
        category = queryset.get(pk=self.category.pk)

        self.assertEqual(category.article_count, 2)

    def test_display_cover_image_without_image(self):

        admin_instance = CategoryAdmin(Category, admin.site)
        value = admin_instance.cover_image(obj=self.category)

        self.assertEqual("-", value)

    def test_display_cover_image_with_image(self):

        self.category.image = "test.jpg"
        self.category.save(update_fields=["image"])

        admin_instance = CategoryAdmin(Category, admin.site)
        value = admin_instance.cover_image(obj=self.category)

        self.assertEqual(
            value, '<img src="/media/test.jpg" style="max-width:70px; max-height:70px">'
        )

    def test_display_thumbnail_without_image(self):

        admin_instance = CategoryAdmin(Category, admin.site)
        value = admin_instance.thumbnail(obj=self.category)

        self.assertEqual("-", value)

    def test_display_thumbnail_with_image(self):

        self.category.image = "test.jpg"
        self.category.save(update_fields=["image"])

        admin_instance = CategoryAdmin(Category, admin.site)
        value = admin_instance.thumbnail(obj=self.category)

        self.assertEqual(
            value,
            '<img src="/media/test.jpg" width="200px" style="object-fit:cover;'
            'border-radius:6px;" />',
        )


class ArticleAdminTest(BaseBlogTest):
    def test_display_thumbnail(self):

        admin_instance = ArticleAdmin(Article, admin.site)
        value = admin_instance.thumbnail(obj=self.create_article())
        self.assertEqual(
            value,
            """<img src="/media/test.jpg" width="250px" height="250px" """
            """style="object-fit:cover;border-radius:6px;" />""",
        )

    def test_save_model_on_change_mode(self):
        article = self.create_article()
        author = article.author

        request = self.get_admin_request()
        admin_instance = ArticleAdmin(Article, admin.site)

        admin_instance.save_model(request, article, ArticleAdminForm, change=True)

        self.assertEqual(author, article.author)

    def test_save_model_on_add_mode(self):
        article = self.create_article()
        author = article.author

        request = self.get_admin_request()
        admin_instance = ArticleAdmin(Article, admin.site)

        admin_instance.save_model(request, article, ArticleAdminForm, change=False)

        self.assertNotEqual(author, article.author)

    def test_save_related(self):
        article = self.create_article()
        request = self.get_admin_request()

        form = Mock()
        form.instance = article

        admin_instance = ArticleAdmin(Article, admin.site)
        admin_instance.save_related(request, form, [], False)

        self.assertIn(article.category_main, article.categories.all())

    def test_action_unpublished_selected(self):

        for i, status in enumerate(
            [
                Article.Status.DRAFT,
                Article.Status.ARCHIVED,
                Article.Status.SCHEDULED,
                Article.Status.PUBLISHED,
            ]
        ):
            self.create_article(status=status, title=f"test {i}")

        request = self.get_admin_request()
        admin_instance = ArticleAdmin(Article, admin.site)

        queryset = Article.objects.all()
        admin_instance.unpublish_selected(request, queryset)

        status = set(a.status for a in Article.objects.all())
        self.assertEqual({Article.Status.ARCHIVED}, status)

    def test_send_message_to_user_for_action_unpublished_selected(self):
        for i, status in enumerate(
            [
                Article.Status.DRAFT,
                Article.Status.ARCHIVED,
                Article.Status.SCHEDULED,
                Article.Status.PUBLISHED,
            ]
        ):
            self.create_article(status=status, title=f"test {i}")

        request = self.get_admin_request()
        admin_instance = ArticleAdmin(Article, admin.site)

        queryset = Article.objects.all()

        with patch.object(admin_instance, "message_user") as mock_message:
            admin_instance.unpublish_selected(request, queryset)

        mock_message.assert_called_once_with(
            request,
            "4 of articles unpublished.",
            messages.ERROR,
        )

    def test_action_published_selected(self):
        for i, status in enumerate(
            [
                Article.Status.DRAFT,
                Article.Status.SCHEDULED,
                Article.Status.ARCHIVED,
                Article.Status.PUBLISHED,
            ]
        ):
            self.create_article(status=status, title=f"test {i}")

        request = self.get_admin_request()
        admin_instance = ArticleAdmin(Article, admin.site)

        queryset = Article.objects.all()
        admin_instance.publish_selected(request, queryset)

        status = set(a.status for a in Article.objects.all())
        self.assertEqual({Article.Status.PUBLISHED}, status)

    def test_send_message_to_user_for_action_published_selected(self):
        for i, status in enumerate(
            [
                Article.Status.DRAFT,
                Article.Status.SCHEDULED,
                Article.Status.ARCHIVED,
                Article.Status.PUBLISHED,
            ]
        ):
            self.create_article(status=status, title=f"test {i}")

        request = self.get_admin_request()
        admin_instance = ArticleAdmin(Article, admin.site)
        queryset = Article.objects.all()

        with patch.object(admin_instance, "message_user") as mock_message:
            admin_instance.publish_selected(request, queryset)

        mock_message.assert_called_once_with(
            request,
            "4 of articles published.",
            messages.SUCCESS,
        )


class TagAdminTest(BaseBlogTest):
    def test_published_article_count_for_tags(self):
        for i, status in enumerate(
            [
                Article.Status.DRAFT,
                Article.Status.PUBLISHED,
                Article.Status.SCHEDULED,
                Article.Status.PUBLISHED,
                Article.Status.ARCHIVED,
            ]
        ):
            self.create_article(status=status, title=f"test {i}")

        request = self.get_admin_request()
        admin_instance = TagAdmin(Tag, admin.site)

        queryset = admin_instance.get_queryset(request)
        tag = queryset.get(pk=self.tag.pk)

        self.assertEqual(tag.article_count, 2)


class CommentAdminTest(BaseBlogTest):
    def test_action_approve_selected(self):
        article = self.create_article()

        for i, status in enumerate(
            [
                Comment.Status.APPROVED,
                Comment.Status.SPAM,
                Comment.Status.PENDING,
            ]
        ):
            Comment.objects.create(
                article=article,
                name=f"test name{i}",
                email=f"test{i}@email.com",
                body="test body",
                status=status,
            )

        comment_count = Comment.objects.all().count()

        request = self.get_admin_request()
        admin_instance = CommentAdmin(Comment, admin.site)

        queryset = Comment.objects.all()

        admin_instance.approve_selected(request, queryset)
        approved_comment_count = Comment.objects.filter(
            status=Comment.Status.APPROVED
        ).count()

        self.assertEqual(approved_comment_count, comment_count)

    def test_send_message_to_user_for_action_approve_selected(self):
        article = self.create_article()
        for i, status in enumerate(
            [
                Comment.Status.APPROVED,
                Comment.Status.SPAM,
                Comment.Status.PENDING,
            ]
        ):
            Comment.objects.create(
                article=article,
                name=f"test name{i}",
                email=f"test{i}@email.com",
                body="test body",
                status=status,
            )
        request = self.get_admin_request()
        admin_instance = CommentAdmin(Comment, admin.site)

        queryset = Comment.objects.all()

        with patch.object(admin_instance, "message_user") as mock_message:
            admin_instance.approve_selected(request, queryset)

        mock_message.assert_called_once_with(
            request, "3 comments Approved.", messages.SUCCESS
        )

    def test_action_pending_selected(self):
        article = self.create_article()
        for i, status in enumerate(
            [
                Comment.Status.APPROVED,
                Comment.Status.SPAM,
                Comment.Status.PENDING,
            ]
        ):
            Comment.objects.create(
                article=article,
                name=f"test name{i}",
                email=f"test{i}@email.com",
                body="test body",
                status=status,
            )

        comment_count = Comment.objects.all().count()

        request = self.get_admin_request()
        admin_instance = CommentAdmin(Comment, admin.site)

        queryset = Comment.objects.all()

        admin_instance.pending_selected(request, queryset)
        pending_comment_count = Comment.objects.filter(
            status=Comment.Status.PENDING
        ).count()

        self.assertEqual(pending_comment_count, comment_count)

    def test_send_message_to_user_for_action_pending_selected(self):
        article = self.create_article()
        for i, status in enumerate(
            [
                Comment.Status.APPROVED,
                Comment.Status.SPAM,
                Comment.Status.PENDING,
            ]
        ):
            Comment.objects.create(
                article=article,
                name=f"test name{i}",
                email=f"test{i}@email.com",
                body="test body",
                status=status,
            )
        request = self.get_admin_request()
        admin_instance = CommentAdmin(Comment, admin.site)

        queryset = Comment.objects.all()

        with patch.object(admin_instance, "message_user") as mock_message:
            admin_instance.pending_selected(request, queryset)

        mock_message.assert_called_once_with(
            request, "3 selected comments marked as Pending!", messages.WARNING
        )

    def test_action_spam_selected(self):
        article = self.create_article()
        for i, status in enumerate(
            [
                Comment.Status.APPROVED,
                Comment.Status.SPAM,
                Comment.Status.PENDING,
            ]
        ):
            Comment.objects.create(
                article=article,
                name=f"test name{i}",
                email=f"test{i}@email.com",
                body="test body",
                status=status,
            )

        comment_count = Comment.objects.all().count()

        request = self.get_admin_request()
        admin_instance = CommentAdmin(Comment, admin.site)

        queryset = Comment.objects.all()

        admin_instance.spam_selected(request, queryset)
        spam_comment_count = Comment.objects.filter(status=Comment.Status.SPAM).count()

        self.assertEqual(spam_comment_count, comment_count)

    def test_send_message_to_user_for_action_spam_selected(self):
        article = self.create_article()
        for i, status in enumerate(
            [
                Comment.Status.APPROVED,
                Comment.Status.SPAM,
                Comment.Status.PENDING,
            ]
        ):
            Comment.objects.create(
                article=article,
                name=f"test name{i}",
                email=f"test{i}@email.com",
                body="test body",
                status=status,
            )
        request = self.get_admin_request()
        admin_instance = CommentAdmin(Comment, admin.site)

        queryset = Comment.objects.all()

        with patch.object(admin_instance, "message_user") as mock_message:
            admin_instance.spam_selected(request, queryset)

        mock_message.assert_called_once_with(
            request, "3 selected comments marked as Spam!", messages.ERROR
        )
