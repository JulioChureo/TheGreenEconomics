import contextlib

from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class PagesConfig(AppConfig):
    name = "the_green_economics.apps.pages"
    verbose_name = _("pages:app_verbose_name")

    def ready(self):
        with contextlib.suppress(ImportError):
            import the_green_economics.apps.pages.signals  # noqa: F401
