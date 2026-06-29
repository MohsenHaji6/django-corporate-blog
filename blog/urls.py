from django.urls import path

from .views import blog_detail_view, blog_list_view, category_list_view

app_name = "blog"

urlpatterns = [
    path("", blog_list_view, name="list"),
    path("<slug:slug>/", blog_detail_view, name="detail"),
    path("cat/<slug:slug>/", category_list_view, name="category"),
]
