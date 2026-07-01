from tinymce.widgets import TinyMCE


class ArticleEditorWidget(TinyMCE):
    default_mce_attrs = {
        "height": 700,
        "width": "100%",
        "menubar": True,
        "branding": False,
        "promotion": False,
        "resize": True,
        "directionality": "rtl",
        "plugins": ("image link lists table code searchreplace preview fullscreen"),
        "toolbar": (
            "undo redo | "
            "blocks | "
            "bold italic underline | "
            "alignleft aligncenter alignright alignjustify | "
            "bullist numlist | "
            "link image table | "
            "code preview fullscreen"
        ),
    }

    def __init__(self, attrs=None, mce_attrs=None):
        editor_attrs = self.default_mce_attrs.copy()

        if mce_attrs:
            editor_attrs.update(mce_attrs)

        super().__init__(
            attrs=attrs,
            mce_attrs=editor_attrs,
        )
