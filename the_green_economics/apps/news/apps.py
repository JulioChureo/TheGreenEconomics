import contextlib

from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class NewsConfig(AppConfig):
    name = "the_green_economics.apps.news"
    verbose_name = _("News")

    def ready(self):
        with contextlib.suppress(ImportError):
            import the_green_economics.apps.news.signals  # noqa: F401
