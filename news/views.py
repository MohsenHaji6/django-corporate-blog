from django.http import JsonResponse
from django.utils.translation import gettext_lazy as _

from .forms import SubscriberForm


def subscriber_view(request):
    if request.method == "POST":
        form = SubscriberForm(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse(
                {"success": True, "message": _("Subscription successful.")}, status=200
            )
        return JsonResponse({"success": False, "errors": form.errors}, status=400)

    return JsonResponse(
        {"success": False, "message": _("Invalid request method.")}, status=405
    )
