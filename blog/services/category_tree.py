from blog.models import Category


def build_category_tree(paths=None):

    if not paths:
        categories = Category.objects.only(
            "pk",
            "name",
            "slug",
            "path",
            "depth",
        )
    else:
        categories = Category.objects.filter(path__in=paths).only(
            "pk",
            "name",
            "slug",
            "path",
            "depth",
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
            "children": [],
        }
        lookup[category.path] = node

        if category.depth == 1:
            tree.append(node)
        else:
            parent_path = category.path[: -Category.steplen]
            lookup[parent_path]["children"].append(node)

    return tree


def build_category_choices(paths=None):
    """
    Output:
    [
        (1, "Technology"),
        (2, "├── Programming"),
        (3, "│   ├── Python"),
        (4, "│   └── Django"),
        (5, "└── Frontend"),
    ]
    """

    tree = build_category_tree(paths)
    choices = []

    def walk(nodes, prefix=""):
        last_index = len(nodes) - 1

        for index, node in enumerate(nodes):
            is_last = index == last_index

            # This node tag
            if prefix:
                label = f"""{prefix}{"\u00a0\u00a0" if is_last else "\u00a0\u00a0"}
                {node["name"]}"""
                # ├── └──
            else:
                label = node["name"]

            choices.append((node["pk"], label))

            # If it has children, create the prefix for the next generation
            if node["children"]:
                next_prefix = prefix + (
                    "\u00a0\u00a0\u00a0\u00a0\u00a0\u00a0\u00a0"
                    if is_last
                    else "\u00a0\u00a0\u00a0\u00a0\u00a0"
                    # │
                )
                walk(node["children"], next_prefix)

    # Roots are processed
    root_last = len(tree) - 1

    for index, root in enumerate(tree):
        is_last_root = index == root_last

        choices.append((root["pk"], root["name"]))

        if root["children"]:
            walk(
                root["children"],
                "" if is_last_root else "\u00a0",
            )

    return choices
