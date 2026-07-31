from django import forms

from .models import ContactMessage, Page
from .widgets import PageEditorWidgets


class ContactMessageForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ["name", "phone_number", "message"]


class AddressAdminForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = "__all__"
        widgets = {
            "address": forms.Textarea(
                attrs={
                    "rows": 4,
                    "cols": 50,
                }
            )
        }


class SiteSettingAdminForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = "__all__"
        widgets = {
            "site_title": forms.TextInput(attrs={"size": "70"}),
            "site_description": forms.Textarea(attrs={"rows": 3, "cols": 72}),
            "hero_title": forms.TextInput(attrs={"size": "70"}),
            "hero_text": forms.Textarea(attrs={"rows": 5, "cols": 72}),
            "meta_title": forms.TextInput(attrs={"size": "70"}),
            "meta_description": forms.Textarea(attrs={"rows": 3, "cols": 72}),
        }


class PageAdminForm(forms.ModelForm):
    class Meta:
        model = Page
        fields = "__all__"
        widgets = {
            "description": PageEditorWidgets(),
            "short_description": forms.Textarea(attrs={"rows": 5, "cols": 150}),
            "meta_title": forms.TextInput(attrs={"size": "70"}),
            "meta_description": forms.Textarea(attrs={"rows": 3, "cols": 72}),
        }
