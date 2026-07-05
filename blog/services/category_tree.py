from blog.models import Category


def build_category_tree():

    categories = Category.objects.only(
        "pk",
        "name",
        "slug",
        "path",
        "depth",
        "numchild",
    )

    tree = []
    lookup = {}
    for category in categories:
        node = {
            "pk": category.pk,
            "name": category.name,
            "slug": category.slug,
            "depth": category.depth,
            "url": category.get_absolute_url(),
            "has_children": category.numchild > 0,
            "children": [],
        }
        lookup[category.path] = node

        if category.depth == 1:
            tree.append(node)
        else:
            parent_path = category.path[: -Category.steplen]
            lookup[parent_path]["children"].append(node)

    return tree
