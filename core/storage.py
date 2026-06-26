from pathlib import Path
from uuid import uuid4

from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.utils import timezone


class CKEditorStorage(FileSystemStorage):
    """
    Storage for images uploaded from CKEditor.
    """

    def __init__(self, *args, **kwargs):
        kwargs.setdefault("location", Path(settings.MEDIA_ROOT) / "ckeditor")
        kwargs.setdefault("base_url", f"{settings.MEDIA_URL}ckeditor/")
        super().__init__(*args, **kwargs)

    def get_available_name(self, name, max_length=None):
        extension = Path(name).suffix.lower()

        today = timezone.now()

        relative_path = Path(
            str(today.year),
            f"{today.month:02}",
            f"{uuid4().hex}{extension}",
        )

        return super().get_available_name(
            str(relative_path),
            max_length=max_length,
        )
