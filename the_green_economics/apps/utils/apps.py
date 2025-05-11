from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class UtilsConfig(AppConfig):
    name = "the_green_economics.apps.utils"
    verbose_name = _("Utils")
