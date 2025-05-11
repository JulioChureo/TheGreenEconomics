from django.views.generic import TemplateView


class DashboardHomeView(TemplateView):
    template_name = "dashboards/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context["articles"] = dashboard_article_list_view.get_queryset(self)
        # context["news"] = dashboard_news_list_view.get_queryset(self)
        return context


dashboard_home_view = DashboardHomeView.as_view()
