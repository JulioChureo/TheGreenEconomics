"""Module for all Form Tests."""

from django.utils.translation import gettext_lazy as _

from the_green_economics.apps.users.forms import UserCreationForm
from the_green_economics.apps.users.models import User


class TestUserCreationForm:
    """
    Test class for all tests related to the UserAdminCreationForm
    """

    def test_username_validation_error_msg(self, user: User):
        """
        Tests UserAdminCreation Form's unique validator functions correctly by testing:
            1) A new user with an existing username cannot be added.
            2) Only 1 error is raised by the UserCreation Form
            3) The desired error message is raised
        """

        # The user already exists,
        # hence cannot be created.
        form = UserCreationForm(
            {
                "username": user.username,
                "password": user.password,
                "email": user.email,
                "name": user.name,
            },
        )

        assert not form.is_valid()
        assert len(form.errors) == 1
        assert "username" in form.errors
        assert form.errors["username"][0] == _("This username has already been taken.")
