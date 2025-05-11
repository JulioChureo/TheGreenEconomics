from django import forms
from django.utils.translation import gettext_lazy as _

from .models import User


class UserCreationForm(forms.ModelForm):
    """User creation form.

    Description: This form is used to create a new user.

    Attributes:
        password (CharField): The password field.
        email (CharField): The email field.
        name (CharField): The name field.

    Methods:
        __init__ (Any): Initializes the form.
        save (Any): Saves the user.

    """

    password = forms.CharField(
        max_length=128,
        required=True,
        label=_("Password"),
        widget=forms.widgets.PasswordInput,
    )

    email = forms.CharField(
        max_length=128, required=True, label=_("Email"), widget=forms.widgets.TextInput
    )

    class Meta:
        model = User
        fields = ("username", "email", "name", "password")


class UserLoginForm(forms.Form):
    """User login form.

    Description: This form is used to log in a user.

    Attributes:
        username (CharField): The username field.
        password (CharField): The password field.

    Methods:
        __init__ (Any): Initializes the form.

    """

    username = forms.CharField(
        max_length=128,
        required=True,
        label=_("Username"),
        widget=forms.widgets.TextInput,
    )

    password = forms.CharField(
        max_length=128,
        required=True,
        label=_("Password"),
        widget=forms.widgets.PasswordInput,
    )


class UserLogOutForm(forms.Form):
    """User logout form.

    Description: This form is used to log out a user.

    Attributes:
        confirmation (BooleanField): The confirmation field.

    Methods:
        __init__ (Any): Initializes the form.

    """

    confirmation = forms.BooleanField(
        required=True, label=_("Confirmation"), widget=forms.widgets.CheckboxInput
    )


class UserUpdateForm(forms.ModelForm):
    """User update form.

    Description: This form is used to update a user.

    Attributes:
        password (CharField): The password field.
        email (CharField): The email field.
        name (CharField): The name field.

    Methods:
        __init__ (Any): Initializes the form.
        save (Any): Saves the user.

    """

    usename = forms.CharField(
        max_length=128,
        required=False,
        label=_("User username"),
        widget=forms.widgets.TextInput,
    )

    email = forms.CharField(
        max_length=128,
        required=False,
        label=_("User email"),
        widget=forms.widgets.TextInput,
    )

    name = forms.CharField(
        max_length=128,
        required=False,
        label=_("User name"),
        widget=forms.widgets.TextInput,
    )

    class Meta:
        model = User
        fields = ("username", "email", "name")
