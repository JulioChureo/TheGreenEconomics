import contextlib

from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class UsersConfig(AppConfig):
    name = "the_green_economics.apps.users"
    verbose_name = _("Users")

    def ready(self):
        with contextlib.suppress(ImportError):
            import the_green_economics.apps.users.signals  # noqa: F401
