import contextlib

from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class HomeConfig(AppConfig):
    name = "the_green_economics.apps.home"
    verbose_name = _("Home")

    def ready(self):
        with contextlib.suppress(ImportError):
            import the_green_economics.apps.home.signals  # noqa: F401
