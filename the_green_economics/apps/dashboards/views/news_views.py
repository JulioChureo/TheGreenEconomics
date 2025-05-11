from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.views.generic import DeleteView
from django.views.generic import DetailView
from django.views.generic import ListView
from django.views.generic import UpdateView

from the_green_economics.apps.news.forms import DeleteNewsForm
from the_green_economics.apps.news.forms import NewsForm
from the_green_economics.apps.news.models import News


class DashboardNewsListView(ListView):
    model = News
    template_name = "dashboards/news/news_list.html"
    context_object_name = "news"

    def get_queryset(self):
        return News.objects.filter().order_by(
            "-publication_date",
        )


dashboard_news_list_view = DashboardNewsListView.as_view()


class DashboardNewsDetailView(DetailView):
    model = News
    template_name = "dashboards/news/news_retrieve.html"
    context_object_name = "news"
    slug_url_kwarg = "slug"

    def get_queryset(self):
        return News.objects.all()


dashboard_news_detail_view = DashboardNewsDetailView.as_view()


class DashboardNewsCreateView(CreateView):
    model = News
    form_class = NewsForm
    template_name = "dashboards/news/news_create.html"
    success_url = reverse_lazy("news:list")


dashboard_news_create_view = DashboardNewsCreateView.as_view()


class DashboardNewsUpdateView(UpdateView):
    model = News
    form_class = NewsForm
    template_name = "dashboards/news/news_update.html"
    success_url = reverse_lazy("news:list")
    slug_url_kwarg = "slug"

    def get_queryset(self):
        return News.objects.all()


dashboard_news_update_view = DashboardNewsUpdateView.as_view()


class DashboardNewsDeleteView(DeleteView):
    model = News
    form_class = DeleteNewsForm
    template_name = "dashboards/news/news_delete.html"
    success_url = reverse_lazy("news:list")
    slug_url_kwarg = "slug"

    def get_queryset(self):
        return News.objects.all()


dashboard_news_delete_view = DashboardNewsDeleteView.as_view()
