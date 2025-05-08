import contextlib

from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class DashboardsConfig(AppConfig):
    name = "the_green_economics.apps.dashboards"
    verbose_name = _("Dashboards")

    def ready(self):
        with contextlib.suppress(ImportError):
            import the_green_economics.apps.dashboards.signals  # noqa
