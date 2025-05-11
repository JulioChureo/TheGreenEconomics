from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import UserPassesTestMixin


class AdminUserMixin(LoginRequiredMixin, UserPassesTestMixin):
    """
    Mixin to restrict access to admin users only.
    Inherits from LoginRequiredMixin and UserPassesTestMixin.
    """

    login_url = "users:login"
    redirect_field_name = "next"
    raise_exception = False
    permission_denied_message = "You do not have permission to access this page."

    def test_func(self):
        if not self.request.user:
            return False
        return self.request.user.is_staff or self.request.user.is_superuser
