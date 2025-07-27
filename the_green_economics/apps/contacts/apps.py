import contextlib

from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class ContactsConfig(AppConfig):
    name = "the_green_economics.apps.contacts"
    verbose_name = _("contacts:app_verbose_name")

    def ready(self):
        with contextlib.suppress(ImportError):
            import the_green_economics.apps.contacts.signals  # noqa: F401
