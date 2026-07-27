from django.contrib import admin

from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ["full_name", "phone_number", "last_login", "is_active"]
    search_fields = ["first_name", "last_name", "phone_number"]
    list_per_page = 10
    list_editable = ["is_active"]
    ordering = ["first_name", "last_name"]

    def full_name(self, obj):
        return f"{obj.get_full_name() or obj.phone_number}"

    def save_model(self, request, obj, form, change):
        if not change:
            obj.set_password(obj.password)
        super().save_model(request, obj, form, change)
