from django.urls import path

from .views import (
    blog_detail_view,
    blog_list_view,
    category_list_view,
    tag_view,
)

app_name = "blog"

urlpatterns = [
    path("", blog_list_view, name="list"),
    path("<str:slug>/", blog_detail_view, name="detail"),
    path("cat/<str:slug>/", category_list_view, name="category"),
    path("tag/<str:slug>/", tag_view, name="tag"),
]
