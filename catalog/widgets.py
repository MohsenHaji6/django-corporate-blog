from tinymce.widgets import TinyMCE


class FeaturesEditorWidget(TinyMCE):
    default_mce_attrs = {
        "height": 220,
        "menubar": False,
        "branding": False,
        "promotion": False,
        "plugins": "lists link",
        "toolbar": ("bold italic underline | bullist numlist | removeformat"),
        "block_formats": "Paragraph=p;",
    }

    def __init__(self, attrs=None, mce_attrs=None):
        editor_attrs = self.default_mce_attrs.copy()
        if mce_attrs:
            editor_attrs.update(mce_attrs)
        super().__init__(attrs=attrs, mce_attrs=editor_attrs)
