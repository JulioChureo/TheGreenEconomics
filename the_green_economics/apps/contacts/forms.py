from captcha.fields import CaptchaField
from django import forms
from django.utils.translation import gettext_lazy as _

from the_green_economics.apps.contacts.models import ResearchProposal


class ResearchProposalForm(forms.ModelForm):
    captcha = CaptchaField()

    class Meta:
        model = ResearchProposal
        fields = [
            "first_name",
            "last_name",
            "email",
            "phone",
            "institution",
            "title",
            "research_area",
            "abstract",
        ]
