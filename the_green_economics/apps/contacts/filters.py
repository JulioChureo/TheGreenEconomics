import django_filters
from django.utils.translation import gettext_lazy as _

from the_green_economics.apps.contacts.models import ResearchProposal
from the_green_economics.apps.contacts.models import ResearchProposalTypes


class ResearchProposalFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(
        label=_("research_proposal:filter_title_label"),
        help_text=_("research_proposal:filter_title_help_text"),
        field_name="title",
        lookup_expr="icontains",
    )
    research_area = django_filters.ChoiceFilter(
        label=_("research_proposal:filter_research_area_label"),
        help_text=_("research_proposal:filter_research_area_help_text"),
        field_name="research_area",
        choices=ResearchProposalTypes,
        lookup_expr="exact",
    )
    first_name = django_filters.CharFilter(
        label=_("research_proposal:filter_first_name_label"),
        help_text=_("research_proposal:filter_first_name_help_text"),
        field_name="first_name",
        lookup_expr="icontains",
    )

    class Meta:
        model = ResearchProposal
        fields = ["title", "research_area", "first_name"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.filters["title"].field.widget.attrs["placeholder"] = kwargs.get(
            "title_placeholder",
            "Buscar por título",
        )
        self.filters["title"].field.widget.attrs["class"] = "w-full"
