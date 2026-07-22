from django.contrib import admin

from .models import Address, ContactMessage, Page, PhoneNumber, SiteSetting, SocialLink


@admin.register(PhoneNumber)
class PhoneNumberAdmin(admin.ModelAdmin):
    list_display = ["use_for", "phone_number"]


@admin.register(SocialLink)
class SocialLinkAdmin(admin.ModelAdmin):
    list_display = ["name"]


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ["name"]


@admin.register(SiteSetting)
class SiteSettingAdmin(admin.ModelAdmin):
    list_display = ["site_title", "site_description"]


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ["name", "phone_number", "message"]


@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    pass
