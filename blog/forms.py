from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from treebeard.forms import MoveNodeForm

from .models import Article, Category, Comment, Tag
from .widgets import ArticleEditorWidget, SummaryEditorWidget


class CategoryAdminForm(MoveNodeForm, forms.ModelForm):
    MAX_DEPTH = 3

    class Meta:
        model = Category
        fields = "__all__"
        widgets = {
            "description": ArticleEditorWidget(),
            "meta_description": forms.Textarea(
                attrs={
                    "rows": 3,
                    "cols": 80,
                }
            ),
            "meta_title": forms.Textarea(
                attrs={
                    "rows": 1,
                    "cols": 80,
                }
            ),
        }

    def clean(self):
        cleaned_data = super().clean()

        target = cleaned_data.get("treebeard_ref_node")
        position = cleaned_data.get("treebeard_position")

        if target:
            # If it is to be listed as a child
            if position in ["sorted-child", "first-child", "last-child"]:
                new_depth = target.depth + 1

                if new_depth > self.MAX_DEPTH:
                    raise ValidationError(
                        _(f"The maximum allowed depth is {self.MAX_DEPTH}")
                    )

        return cleaned_data


class TagAdminForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = "__all__"
        widgets = {
            "description": ArticleEditorWidget(),
            "meta_description": forms.Textarea(
                attrs={
                    "rows": 3,
                    "cols": 80,
                }
            ),
            "meta_title": forms.Textarea(
                attrs={
                    "rows": 1,
                    "cols": 80,
                }
            ),
        }


class ArticleAdminForm(forms.ModelForm):
    class Meta:
        model = Article

        fields = "__all__"

        widgets = {
            "content": ArticleEditorWidget(),
            "summary": SummaryEditorWidget(),
            "meta_description": forms.Textarea(
                attrs={
                    "rows": 3,
                    "cols": 80,
                }
            ),
            "meta_title": forms.Textarea(
                attrs={
                    "rows": 1,
                    "cols": 80,
                }
            ),
        }


class CommentAdminForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = "__all__"

        widgets = {
            "body": forms.Textarea(
                attrs={
                    "rows": 5,
                    "cols": 50,
                }
            ),
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment

        fields = ["name", "email", "body"]
