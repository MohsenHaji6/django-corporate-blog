from django.urls import path

from .views import (
    blog_category_list_view,
    blog_detail_view,
    blog_list_view,
    blog_tag_list_view,
)

app_name = "blog"

urlpatterns = [
    path("", blog_list_view, name="list"),
    path("<str:slug>/", blog_detail_view, name="detail"),
    path("cat/<str:slug>/", blog_category_list_view, name="category"),
    path("tag/<str:slug>/", blog_tag_list_view, name="tag"),
]
