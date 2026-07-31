from tinymce.widgets import TinyMCE


class PageEditorWidgets(TinyMCE):
    default_mce_attrs = {
        "height": 700,
        "width": "100%",
        "menubar": False,
        "branding": False,
        "promotion": False,
        "resize": True,
        "directionality": "ltr",
        "plugins": ("image link lists table code searchreplace preview fullscreen"),
        "toolbar1": (
            "undo redo | "
            "blocks | "
            "bold italic underline strikethrough | "
            "blockquote hr | "
            "alignleft aligncenter alignright alignjustify | "
        ),
        "toolbar2": (
            "bullist numlist | "
            "forecolor backcolor | "
            "link image table | "
            "searchreplace code preview fullscreen"
        ),
        "block_formats": (
            "Paragraph=p;"
            "Heading 2=h2;"
            "Heading 3=h3;"
            "Heading 4=h4;"
            "Heading 5=h5;"
            "Preformatted=pre"
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
