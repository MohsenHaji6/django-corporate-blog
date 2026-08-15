from django.contrib import admin

from blog.tests.base import BaseBlogTest
from core.admin import (
    ContactMessageAdmin,
    PhoneNumberAdmin,
    SiteSettingAdmin,
    SocialLinkAdmin,
)
from core.models import ContactMessage, PhoneNumber, SiteSetting, SocialLink

from .base import BaseCoreTest


class PhoneNumberAdminTest(BaseCoreTest):
    def test_thumbnail_with_icon(self):
        phone = self.create_phone_number()

        phone.icon = "phone/test-icon.jpg"  # type: ignore
        phone.save(update_fields=["icon"])

        admin_instance = PhoneNumberAdmin(PhoneNumber, admin.site)

        result = admin_instance.thumbnail(phone)

        self.assertEqual(
            result,
            '<img src="/media/phone/test-icon.jpg" width="35px" >',
        )

    def test_thumbnail_without_icon(self):
        phone = self.create_phone_number()

        admin_instance = PhoneNumberAdmin(PhoneNumber, admin.site)

        result = admin_instance.thumbnail(phone)

        self.assertEqual(result, "-")


class SocialLinkAdminTest(BaseCoreTest):
    def test_thumbnail_with_icon(self):
        social_link = self.create_social_link()

        social_link.icon = "social/test-icon.jpg"  # type: ignore
        social_link.save(update_fields=["icon"])

        admin_instance = SocialLinkAdmin(SocialLink, admin.site)

        result = admin_instance.thumbnail(social_link)

        self.assertEqual(
            result,
            '<img src="/media/social/test-icon.jpg" width="35px" >',
        )

    def test_thumbnail_without_icon(self):
        social_link = self.create_social_link()

        admin_instance = SocialLinkAdmin(SocialLink, admin.site)

        result = admin_instance.thumbnail(social_link)

        self.assertEqual(result, "-")


class SiteSettingAdminTest(BaseCoreTest):
    def test_hero_thumbnail_with_image(self):
        site_setting = SiteSetting.objects.get()

        site_setting.hero_image = "site/test-hero.jpg"  # type: ignore
        site_setting.save(update_fields=["hero_image"])

        admin_instance = SiteSettingAdmin(SiteSetting, admin.site)

        result = admin_instance.hero_thumbnail(site_setting)

        self.assertEqual(
            result,
            '<img src="/media/site/test-hero.jpg" width="200px" >',
        )

    def test_hero_thumbnail_without_image(self):
        site_setting = SiteSetting.objects.get()

        site_setting.hero_image = ""  # type: ignore
        site_setting.save(update_fields=["hero_image"])

        admin_instance = SiteSettingAdmin(SiteSetting, admin.site)

        result = admin_instance.hero_thumbnail(site_setting)

        self.assertEqual(result, "-")

    def test_logo_thumbnail_with_image(self):
        site_setting = SiteSetting.objects.get()

        site_setting.logo = "logo/test-logo.jpg"  # type: ignore
        site_setting.save(update_fields=["logo"])

        admin_instance = SiteSettingAdmin(SiteSetting, admin.site)

        result = admin_instance.logo_thumbnail(site_setting)

        self.assertEqual(
            result,
            '<img src="/media/logo/test-logo.jpg" width="150px" >',
        )

    def test_logo_thumbnail_without_image(self):
        site_setting = SiteSetting.objects.get()

        site_setting.logo = ""  # type: ignore
        site_setting.save(update_fields=["logo"])

        admin_instance = SiteSettingAdmin(SiteSetting, admin.site)

        result = admin_instance.logo_thumbnail(site_setting)

        self.assertEqual(result, "-")

    def test_favicon_thumbnail_with_image(self):
        site_setting = SiteSetting.objects.get()

        site_setting.favicon = "logo/test-favicon.jpg"  # type: ignore
        site_setting.save(update_fields=["favicon"])

        admin_instance = SiteSettingAdmin(SiteSetting, admin.site)

        result = admin_instance.favicon_thumbnail(site_setting)

        self.assertEqual(
            result,
            '<img src="/media/logo/test-favicon.jpg" width="35px" >',
        )

    def test_favicon_thumbnail_without_image(self):
        site_setting = SiteSetting.objects.get()

        site_setting.favicon = ""  # type: ignore
        site_setting.save(update_fields=["favicon"])

        admin_instance = SiteSettingAdmin(SiteSetting, admin.site)

        result = admin_instance.favicon_thumbnail(site_setting)

        self.assertEqual(result, "-")


class ContactMessageAdminTest(BaseCoreTest, BaseBlogTest):
    def test_user_cannot_add_contact_message_from_admin(self):
        request = self.get_admin_request()

        admin_instance = ContactMessageAdmin(
            ContactMessage,
            admin.site,
        )

        self.assertFalse(admin_instance.has_add_permission(request))


class AdminOrderTest(BaseCoreTest, BaseBlogTest):
    def test_admin_apps_are_ordered(self):
        request = self.get_admin_request()

        app_list = admin.site.get_app_list(request)

        app_names = [app["name"] for app in app_list]

        self.assertEqual(
            app_names,
            [
                "Core",
                "Accounts",
                "Catalog",
                "Blog",
                "Marketing",
                "Authentication and Authorization",
            ],
        )

    def test_core_models_are_ordered(self):
        request = self.get_admin_request()

        app_list = admin.site.get_app_list(request)

        core = next(app for app in app_list if app["name"] == "Core")

        self.assertEqual(
            [model["object_name"] for model in core["models"]],
            [
                "SiteSetting",
                "ContactMessage",
                "Page",
                "PhoneNumber",
                "SocialLink",
                "Address",
            ],
        )
