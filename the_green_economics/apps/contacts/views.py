from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.utils.translation import gettext_lazy as _
from django.views.generic import CreateView
from honeypot.decorators import check_honeypot

from the_green_economics.apps.contacts.forms import ResearchProposalForm
from the_green_economics.apps.contacts.models import ResearchProposal


@method_decorator(check_honeypot, name="post")
class ResearchProposalCreateView(CreateView, SuccessMessageMixin):
    model = ResearchProposal
    form_class = ResearchProposalForm
    template_name = "contacts/research_proposal_create.html"
    success_url = reverse_lazy("contacts:create")
    success_message = _("Your research proposal has been submitted successfully.")


research_proposal_create_view = ResearchProposalCreateView.as_view()
