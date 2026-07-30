from django import forms

from .models import ProductVariant
from .widgets import FeaturesEditorWidget


class ProductVariantAdminForm(forms.ModelForm):
    class Meta:
        model = ProductVariant
        fields = "__all__"
        widgets = {"features": FeaturesEditorWidget()}
