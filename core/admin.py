from django.contrib import admin

from .models import Address, PhoneNumber, SiteSetting, SocialMedia


class PhoneNumberInline(admin.TabularInline):
    """Tabular Inline View for PhoneNumber"""

    model = PhoneNumber
    max_num = 5
    extra = 1


class SocialMediaInline(admin.TabularInline):
    """Tabular Inline View for SocialMedia"""

    model = SocialMedia
    max_num = 5
    extra = 1


class AddressInline(admin.TabularInline):
    """Tabular Inline View for Address"""

    model = Address
    max_num = 5
    extra = 1


@admin.register(SiteSetting)
class SiteSettingAdmin(admin.ModelAdmin):
    list_display = ["title", "description"]
    inlines = [PhoneNumberInline, SocialMediaInline, AddressInline]
