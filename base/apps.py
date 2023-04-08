# Django Imports
from django.apps import AppConfig


class SrcConfig(AppConfig):
    """Django Apps Config class"""

    name = "base"

    def ready(self):
        from . import signals
