from django.views.generic import DetailView

from the_green_economics.apps.contacts.filters import ResearchProposalFilter
from the_green_economics.apps.contacts.models import ResearchProposal
from the_green_economics.apps.utils.mixins import AdminUserMixin
from the_green_economics.apps.utils.mixins import PaginatedFilteredListView

RESEARCH_PROPOSAL_QUERYSET = ResearchProposal.objects.all()


class DashboardResearchProposalListView(AdminUserMixin, PaginatedFilteredListView):
    model = ResearchProposal
    template_name = "dashboards/contacts/research_proposal_list.html"
    context_object_name = "research_proposals"
    queryset = RESEARCH_PROPOSAL_QUERYSET
    paginate_by = 10
    filterset_class = ResearchProposalFilter


dashboard_research_proposal_list_view = DashboardResearchProposalListView.as_view()


class DashboardResearchProposalDetailView(AdminUserMixin, DetailView):
    model = ResearchProposal
    template_name = "dashboards/contacts/research_proposal_detail.html"
    context_object_name = "research_proposal"
    slug_url_kwarg = "pk"
    queryset = RESEARCH_PROPOSAL_QUERYSET


dashboard_research_proposal_detail_view = DashboardResearchProposalDetailView.as_view()
