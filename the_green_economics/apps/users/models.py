from django.contrib.auth.models import AbstractUser
from django.db.models import CharField
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    """User model for the_green_economics.

    Description: This model is used to store user information.

    Attributes:
        name (CharField): The name of the user.
        first_name (CharField): The first name of the user.
        last_name (CharField): The last name of the user.

    Methods:
        __str__ (str): Returns the string representation of the user.
        get_absolute_url (str): Returns the URL for the user's detail view.

    """

    name = CharField(
        verbose_name=_("user:model_name_verbose_name"),
        help_text=_("user:model_name_help_text"),
        max_length=255,
    )

    def __str__(self) -> str:
        return f"User(pk={self.pk}, username={self.username})"

    def get_absolute_url(self) -> str:
        """Get URL for user's detail view.

        Returns:
            str: URL for user detail.

        """
        return reverse("users:detail", kwargs={"username": self.username})
