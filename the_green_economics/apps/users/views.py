from typing import Any

from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import QuerySet
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.views.generic import CreateView
from django.views.generic import DetailView
from django.views.generic import FormView
from django.views.generic import RedirectView
from django.views.generic import UpdateView

from the_green_economics.apps.users.models import User

from .forms import UserCreationForm
from .forms import UserLoginForm
from .forms import UserLogOutForm


class UserCreateView(CreateView):
    """Create user view.

    Description: This view is used to create a new user.

    Attributes:
        model (User): The model used to create the user.
        form_class (UserCreationForm): The form used to create the user.
        template_name (str): The template used to render the view.
        success_url (str): The URL to redirect to after the user is created.

    Methods:
        get_object (Any): Returns the object to be created.
        get_success_url (str): Returns the URL to redirect to after the user is created.
    """

    model = User
    form_class = UserCreationForm
    template_name = "users/views/user_create.html"

    def get_object(self, queryset: Any):
        return super().get_object(queryset)

    def get_success_url(self) -> str:
        return reverse("users:login")


user_create_view = UserCreateView.as_view()


class UserLoginFormView(FormView):
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
    template_name = "users/views/user_login.html"

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
        return reverse("users:me")

    def form_valid(self, form: UserLoginForm):
        """Check credentials and log in user.

        Description: This method is used to check the credentials of the user and log in the user if they are valid.

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


user_login_view = UserLoginFormView.as_view()


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

    template_name = "users/views/user_logout.html"
    form_class = UserLogOutForm
    success_message = _("Successfully logged out")

    def get_success_url(self):
        return reverse("home")

    def form_valid(self, form):
        logout(self.request)
        return super().form_valid(form)


user_log_out_view = UserLogOutView.as_view()


class UserDetailView(LoginRequiredMixin, DetailView):
    """User detail view.

    Description: This view is used to display the details of a user.

    Attributes:
        model (User): The model used to display the details of a user.
        slug_field (str): The field used to generate the URL for the user.
        slug_url_kwarg (str): The URL argument used to generate the URL for the user.
        template_name (str): The template used to render the view.

    Methods:
        get_object (Any): Returns the user to be displayed.

    """

    model = User
    slug_field = "username"
    slug_url_kwarg = "username"
    template_name = "users/views/user_detail.html"

    def get_object(self):
        return self.request.user


user_detail_view = UserDetailView.as_view()


class UserUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    """User update view.

    Description: This view is used to update the details of a user.

    Attributes:
        model (User): The model used to update the details of a user.
        fields (list): The fields to be updated.
        success_message (str): The message to display after the user is updated.

    Methods:
        get_success_url (str): Returns the URL to redirect to after the user is updated.
        get_object (Any): Returns the user to be updated.

    """

    model = User
    fields = ["name"]
    success_message = _("Information successfully updated")
    template_name = "users/views/user_update.html"

    def get_success_url(self) -> str:
        assert self.request.user.is_authenticated  # type guard
        return self.request.user.get_absolute_url()

    def get_object(self, queryset: QuerySet | None = None) -> User:
        assert self.request.user.is_authenticated  # type guard
        return self.request.user


user_update_view = UserUpdateView.as_view()


class UserRedirectView(LoginRequiredMixin, RedirectView):
    """User redirect view.

    Description: This view is used to redirect a user to their profile page.

    Attributes:
        permanent (bool): Whether the redirect should be permanent.

    Methods:
        get_redirect_url (str): Returns the URL to redirect to.

    """

    permanent = False

    def get_redirect_url(self) -> str:
        return reverse("users:detail", kwargs={"username": self.request.user.username})


user_redirect_view = UserRedirectView.as_view()
