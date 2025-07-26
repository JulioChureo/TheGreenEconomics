from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.views.generic import DeleteView
from django.views.generic import DetailView
from django.views.generic import ListView
from django.views.generic import UpdateView

from the_green_economics.apps.news.forms import DeleteNewsForm
from the_green_economics.apps.news.forms import NewsForm
from the_green_economics.apps.news.models import News
from the_green_economics.apps.utils.mixins import AdminUserMixin
from the_green_economics.apps.utils.models import PublicationStatus

DASHBOARD_NEWS_QUERYSET = News.objects.filter(
    Q(status=PublicationStatus.PUBLISHED) | Q(status=PublicationStatus.DRAFT),
).order_by("-publication_date")


class DashboardNewsListView(AdminUserMixin, ListView):
    model = News
    template_name = "dashboards/news/news_list.html"
    context_object_name = "news"
    queryset = DASHBOARD_NEWS_QUERYSET
    paginate_by = 10
    paginator_class = Paginator


dashboard_news_list_view = DashboardNewsListView.as_view()


class DashboardNewsDetailView(AdminUserMixin, DetailView):
    model = News
    template_name = "dashboards/news/new_detail.html"
    context_object_name = "news"
    slug_url_kwarg = "slug"
    queryset = DASHBOARD_NEWS_QUERYSET


dashboard_news_detail_view = DashboardNewsDetailView.as_view()


class DashboardNewsCreateView(AdminUserMixin, CreateView):
    model = News
    form_class = NewsForm
    template_name = "dashboards/news/news_create.html"
    success_url = reverse_lazy("news:list")
    queryset = DASHBOARD_NEWS_QUERYSET


dashboard_news_create_view = DashboardNewsCreateView.as_view()


class DashboardNewsUpdateView(AdminUserMixin, UpdateView):
    model = News
    form_class = NewsForm
    template_name = "dashboards/news/news_update.html"
    success_url = reverse_lazy("news:list")
    slug_url_kwarg = "slug"
    queryset = DASHBOARD_NEWS_QUERYSET


dashboard_news_update_view = DashboardNewsUpdateView.as_view()


class DashboardNewsDeleteView(AdminUserMixin, DeleteView):
    model = News
    form_class = DeleteNewsForm
    template_name = "dashboards/news/news_delete.html"
    success_url = reverse_lazy("news:list")
    slug_url_kwarg = "slug"
    queryset = DASHBOARD_NEWS_QUERYSET

    def form_valid(self, form):
        success_url = self.get_success_url()
        self.object = self.get_object()
        self.object.status = PublicationStatus.ARCHIVED
        self.object.save()
        return HttpResponseRedirect(success_url)


dashboard_news_delete_view = DashboardNewsDeleteView.as_view()
