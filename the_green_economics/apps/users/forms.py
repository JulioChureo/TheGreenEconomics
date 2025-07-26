from django import forms
from django.core.validators import EmailValidator
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
        label=_("user:form_password_label"),
        help_text=_("user:form_password_help_text"),
        max_length=128,
        required=True,
        widget=forms.widgets.PasswordInput,
    )

    email = forms.CharField(
        label=_("user:form_email_label"),
        help_text=_("user:form_email_help_text"),
        max_length=128,
        required=True,
        widget=forms.widgets.TextInput,
        validators=[
            EmailValidator(
                message=_("user:form_email_invalid"),
                code="invalid_email",
            ),
        ],
    )

    class Meta:
        model = User
        fields = ("username", "email", "name", "password")
        labels = {
            "username": _("user:form_username_label"),
            "name": _("user:form_name_label"),
        }
        help_texts = {
            "username": _("user:form_username_help_text"),
            "name": _("user:form_name_help_text"),
        }


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
        label=_("user:form_username_label"),
        help_text=_("user:form_username_help_text"),
        max_length=128,
        required=True,
        widget=forms.widgets.TextInput,
    )

    password = forms.CharField(
        label=_("user:form_password_label"),
        help_text=_("user:form_password_help_text"),
        max_length=128,
        required=True,
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
        label=_("user:form_logout_confirmation_label"),
        help_text=_("user:form_logout_confirmation_help_text"),
        required=True,
        widget=forms.widgets.CheckboxInput,
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

    username = forms.CharField(
        label=_("user:form_username_label"),
        help_text=_("user:form_username_help_text"),
        max_length=128,
        required=False,
        widget=forms.widgets.TextInput,
    )

    email = forms.CharField(
        label=_("user:form_email_label"),
        help_text=_("user:form_email_help_text"),
        max_length=128,
        required=False,
        widget=forms.widgets.TextInput,
    )

    name = forms.CharField(
        label=_("user:form_name_label"),
        help_text=_("user:form_name_help_text"),
        max_length=128,
        required=False,
        widget=forms.widgets.TextInput,
    )

    class Meta:
        model = User
        fields = ("username", "email", "name")
