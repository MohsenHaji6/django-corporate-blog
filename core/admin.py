from django.contrib import admin
from django.http import HttpRequest
from django.utils.html import format_html

from .forms import AddressAdminForm, PageAdminForm, SiteSettingAdminForm
from .models import Address, ContactMessage, Page, PhoneNumber, SiteSetting, SocialLink


@admin.register(PhoneNumber)
class PhoneNumberAdmin(admin.ModelAdmin):
    list_display = [
        "use_for",
        "phone_number",
        "is_primary",
        "is_active",
        "thumbnail",
    ]
    list_editable = ["is_active", "is_primary"]
    readonly_fields = ["thumbnail"]

    fieldsets = (
        (
            "",
            {
                "fields": (
                    "use_for",
                    "phone_number",
                    "icon",
                    "thumbnail",
                    "is_primary",
                    "is_active",
                    "display_order",
                )
            },
        ),
    )

    @admin.display(description="thumbnail")
    def thumbnail(self, obj):
        if obj.icon:
            return format_html('<img src="{}" width="35px" >', obj.icon.url)
        return "-"


@admin.register(SocialLink)
class SocialLinkAdmin(admin.ModelAdmin):
    list_display = ["name", "url", "is_active", "thumbnail"]
    readonly_fields = ["thumbnail"]
    list_editable = ["url", "is_active"]
    fieldsets = (
        (
            "",
            {
                "fields": (
                    "name",
                    "url",
                    "icon",
                    "thumbnail",
                    "display_order",
                    "is_active",
                )
            },
        ),
    )

    @admin.display(description="thumbnail")
    def thumbnail(self, obj):
        if obj.icon:
            return format_html('<img src="{}" width="35px" >', obj.icon.url)
        return "-"


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    form = AddressAdminForm
    list_display = ["name", "is_primary", "is_active"]
    list_editable = ["is_active", "is_primary"]


@admin.register(SiteSetting)
class SiteSettingAdmin(admin.ModelAdmin):
    form = SiteSettingAdminForm
    list_display = ["site_title", "site_description"]
    readonly_fields = ["hero_thumbnail", "logo_thumbnail", "favicon_thumbnail"]

    fieldsets = (
        (
            "Site",
            {
                "fields": (
                    "site_title",
                    "site_description",
                    "email",
                    "answer_hours",
                )
            },
        ),
        (
            "Hero",
            {
                "fields": (
                    "hero_title",
                    "hero_text",
                    "hero_image",
                    "hero_thumbnail",
                )
            },
        ),
        (
            "SEO",
            {
                "fields": (
                    "meta_title",
                    "meta_description",
                )
            },
        ),
        (
            "Visual identity",
            {
                "fields": (
                    "logo",
                    "logo_thumbnail",
                    "favicon",
                    "favicon_thumbnail",
                )
            },
        ),
        ("Copyright", {"fields": ("copyright",)}),
    )

    @admin.display(description="hero thumbnail")
    def hero_thumbnail(self, obj):
        if obj.hero_image:
            return format_html('<img src="{}" width="200px" >', obj.hero_image.url)
        return "-"

    @admin.display(description="logo thumbnail")
    def logo_thumbnail(self, obj):
        if obj.logo:
            return format_html('<img src="{}" width="150px" >', obj.logo.url)
        return "-"

    @admin.display(description="favicon thumbnail")
    def favicon_thumbnail(self, obj):
        if obj.favicon:
            return format_html('<img src="{}" width="35px" >', obj.favicon.url)
        return "-"


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "phone_number",
        "message",
        "email_sent",
        "sms_sent",
        "created_at",
    ]
    search_fields = ["name", "phone_number", "message"]
    list_filter = ["created_at"]

    def has_add_permission(self, request: HttpRequest) -> bool:
        return False


@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    form = PageAdminForm
