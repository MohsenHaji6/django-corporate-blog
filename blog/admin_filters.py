from django.contrib import admin

from .services import build_category_choices


class CategoryDropdownFilter(admin.SimpleListFilter):
    title = "Category"
    parameter_name = "category"

    def lookups(self, request, model_admin):
        return build_category_choices()

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(category_main=self.value())

        return queryset
