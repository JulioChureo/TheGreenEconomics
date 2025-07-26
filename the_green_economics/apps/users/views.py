from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.views.generic import FormView

from the_green_economics.apps.users.forms import UserLoginForm
from the_green_economics.apps.users.forms import UserLogOutForm


class UserLoginView(FormView):
    """Login form view.

    Description: This view is used to log in a user.

    Attributes:
        form_class (UserLoginForm): The form used to log in the user.
        template_name (str): The template used to render the view.
        success_url (str): The URL to redirect to after the user is logged in.

    Methods:
        get_success_url (str): Returns the URL to redirect to after the user is logged in.
        form_valid (Any): Checks the credentials of the user and logs in the user if they are valid.

    """

    form_class = UserLoginForm
    template_name = "users/user_login.html"

    def get_success_url(self) -> str:
        """Get the URL to redirect to after the user is logged in.

        Description: This method is used to get the URL to redirect to after the user is logged in.
            If the user is already logged in, it redirects them to their profile page.
            Otherwise, it redirects them to the login page.

        Returns:
            str: The URL to redirect to after the user is logged in.
        """

        if not self.request.user.is_authenticated:
            return reverse("users:create")
        if self.request.GET["next"]:
            return self.request.GET["next"]
        return reverse("dashboards:home")

    def form_valid(self, form: UserLoginForm):
        """Check credentials and log in user.

        Description: This method is used to check the credentials of the user and log in
        the user if they are valid.

        Args:
            form (UserLoginForm): The form used to log in the user.

        Returns:
            Any: The response to be returned after the user is logged in.
        """

        user = authenticate(
            request=self.request,
            username=form.cleaned_data["username"],
            password=form.cleaned_data["password"],
        )
        if user is None:
            return super().form_invalid(form)
        login(
            request=self.request,
            user=user,
            backend="django.contrib.auth.backends.ModelBackend",
        )
        return super().form_valid(form)


user_login_view = UserLoginView.as_view()


class UserLogOutView(FormView, LoginRequiredMixin, SuccessMessageMixin):
    """Logout view.

    Description: This view is used to log out a user.

    Attributes:
        template_name (str): The template used to render the view.
        form_class (UserLogOutForm): The form used to log out the user.
        success_message (str): The message to display after the user is logged out.

    Methods:
        get_success_url (str): Returns the URL to redirect to after the user is logged out.
        form_valid (Any): Logs out the user.

    """

    template_name = "users/user_logout.html"
    form_class = UserLogOutForm
    success_message = _("user:view_logout_success_message")

    def get_success_url(self):
        return reverse("home")

    def form_valid(self, form):
        logout(self.request)
        return super().form_valid(form)


user_log_out_view = UserLogOutView.as_view()
