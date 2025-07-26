from django.utils.translation import gettext_lazy as _
from django_filters import CharFilter
from django_filters import DateFilter
from django_filters import FilterSet
from django_filters import OrderingFilter

from the_green_economics.apps.users.models import User


class UserFilter(FilterSet):
    username = CharFilter(
        label=_("user:filter_username_label"),
        help_text=_("user:filter_username_help_text"),
        lookup_expr="icontains",
    )
    date_joined = DateFilter(
        label=_("user:filter_date_joined_label"),
        help_text=_("user:filter_date_joined_help_text"),
        lookup_expr="date",
    )
    last_login = DateFilter(
        label=_("user:filter_last_login_label"),
        help_text=_("user:filter_last_login_help_text"),
        lookup_expr="date",
    )
    is_active = OrderingFilter(
        label=_("user:filter_is_active_label"),
        help_text=_("user:filter_is_active_help_text"),
        fields=("is_active",),
    )

    class Meta:
        model = User
        fields = [
            "username",
            "date_joined",
            "last_login",
            "is_active",
        ]
