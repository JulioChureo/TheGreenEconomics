from django.utils.translation import gettext_lazy as _
from django_filters import CharFilter
from django_filters import DateFilter
from django_filters import FilterSet
from django_filters import OrderingFilter

from the_green_economics.apps.users.models import User


class UserFilter(FilterSet):
    username = CharFilter(lookup_expr="icontains", label=_("User username"))
    date_joined = DateFilter(lookup_expr="date", label=_("User data joined"))
    last_login = DateFilter(lookup_expr="date", label=_("User last login"))
    is_active = OrderingFilter(fields=("is_active",), label=_("User active"))

    class Meta:
        model = User
        fields = [
            "username",
            "date_joined",
            "last_login",
            "is_active",
        ]
