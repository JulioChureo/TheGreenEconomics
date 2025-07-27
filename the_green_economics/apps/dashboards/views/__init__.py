from django.views.generic import TemplateView

from the_green_economics.apps.utils.mixins import AdminUserMixin


class DashboardHomeView(TemplateView, AdminUserMixin):
    template_name = "dashboards/home.html"

    # def get_context_data(self, **kwargs):
    #    context = super().get_context_data(**kwargs)
    #    return context


dashboard_home_view = DashboardHomeView.as_view()
