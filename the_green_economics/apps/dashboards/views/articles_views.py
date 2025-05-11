from django.core.paginator import Paginator
from django.db.models import Q
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.views.generic import DeleteView
from django.views.generic import DetailView
from django.views.generic import ListView
from django.views.generic import UpdateView

from the_green_economics.apps.articles.forms import ArticleForm
from the_green_economics.apps.articles.forms import DeleteArticleForm
from the_green_economics.apps.articles.models import Article
from the_green_economics.apps.utils.mixins import AdminUserMixin

DASHBOARD_ARTICLES_QUERYSET = Article.objects.filter(
    Q(status=Article.Status.PUBLISHED)
    | Q(status=Article.Status.DRAFT)
    | Q(status=Article.Status.UNDER_REVIEW),
).order_by("-updated_at")


class DashboardArticleListView(AdminUserMixin, ListView):
    model = Article
    template_name = "dashboards/articles/article_list.html"
    context_object_name = "articles"
    queryset = DASHBOARD_ARTICLES_QUERYSET
    paginator_class = Paginator
    paginate_by = 10


dashboard_article_list_view = DashboardArticleListView.as_view()


class DashboardArticleDetailView(AdminUserMixin, DetailView):
    model = Article
    template_name = "dashboards/articles/article_retrieve.html"
    context_object_name = "article"
    slug_url_kwarg = "slug"
    queryset = DASHBOARD_ARTICLES_QUERYSET


dashboard_article_detail_view = DashboardArticleDetailView.as_view()


class DashboardArticleCreateView(AdminUserMixin, CreateView):
    model = Article
    form_class = ArticleForm
    template_name = "dashboards/articles/article_create.html"
    success_url = reverse_lazy("articles:list")
    queryset = DASHBOARD_ARTICLES_QUERYSET


dashboard_article_create_view = DashboardArticleCreateView.as_view()


class DashboardArticleUpdateView(AdminUserMixin, UpdateView):
    model = Article
    form_class = ArticleForm
    template_name = "dashboards/articles/article_update.html"
    success_url = reverse_lazy("articles:list")
    slug_url_kwarg = "slug"
    context_object_name = "article"
    queryset = DASHBOARD_ARTICLES_QUERYSET


dashboard_article_update_view = DashboardArticleUpdateView.as_view()


class DashboardArticleDeleteView(AdminUserMixin, DeleteView):
    model = Article
    form_class = DeleteArticleForm
    template_name = "dashboards/articles/article_delete.html"
    success_url = reverse_lazy("articles:list")
    slug_url_kwarg = "slug"
    queryset = DASHBOARD_ARTICLES_QUERYSET


dashboard_article_delete_view = DashboardArticleDeleteView.as_view()
