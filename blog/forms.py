from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from treebeard.forms import MoveNodeForm

from .models import Article
from .widgets import ArticleEditorWidget


class CategoryAdminForm(MoveNodeForm):
    MAX_DEPTH = 3

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


class ArticleAdminForm(forms.ModelForm):
    class Meta:
        model = Article

        fields = "__all__"

        widgets = {
            "content": ArticleEditorWidget(),
        }
