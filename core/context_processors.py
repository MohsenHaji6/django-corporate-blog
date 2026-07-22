# Site setting
from .models import Address, PhoneNumber, SiteSetting, SocialLink


def site_setting(request):
    setting = SiteSetting.objects.first()
    address = Address.objects.filter(is_active=True, is_primary=True).first()
    phone = PhoneNumber.objects.filter(is_active=True, is_primary=True).first()
    social_links = SocialLink.objects.all()

    return {
        "setting": setting,
        "phone": phone,
        "address": address,
        "social_links": social_links,
    }
