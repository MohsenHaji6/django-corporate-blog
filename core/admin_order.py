from django.contrib import admin

admin.site.site_header = "Website administration"
admin.site.index_title = "Your Website Name"

APP_ORDER = {
    "Core": 1,
    "Accounts": 2,
    "Catalog": 3,
    "Blog": 4,
    "Marketing": 5,
}


MODEL_ORDER = {
    # Core
    "SiteSetting": 1,
    "ContactMessage": 2,
    "Page": 3,
    "PhoneNumber": 4,
    "SocialLink": 5,
    "Address": 6,
    # Accounts
    "User": 1,
    # Blog
    "Category": 1,
    "Tag": 2,
    "Article": 3,
    "Comment": 4,
    # Catalog
    "Product": 1,
    "ProductVariant": 2,
    # Marketing
    "Subscriber": 1,
}


original_get_app_list = admin.site.get_app_list


def custom_get_app_list(request, app_label=None):
    app_list = original_get_app_list(request, app_label)  # type: ignore

    # Sorting models within each app
    for app in app_list:
        app["models"].sort(key=lambda model: MODEL_ORDER.get(model["object_name"], 999))

    # Sorting apps
    app_list.sort(key=lambda app: APP_ORDER.get(app["name"], 999))

    return app_list


admin.site.get_app_list = custom_get_app_list
