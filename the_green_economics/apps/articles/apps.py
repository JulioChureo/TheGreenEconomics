import contextlib

from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class ArticlesConfig(AppConfig):
    name = "the_green_economics.apps.articles"
    verbose_name = _("article:app_verbose_name")

    def ready(self):
        with contextlib.suppress(ImportError):
            import the_green_economics.apps.articles.signals  # noqa: F401
