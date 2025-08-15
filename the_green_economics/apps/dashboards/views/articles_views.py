from django.db.models import Q
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.views.generic import DeleteView
from django.views.generic import DetailView
from django.views.generic import UpdateView

from the_green_economics.apps.articles.filters import ArticleFilter
from the_green_economics.apps.articles.forms import ArticleForm
from the_green_economics.apps.articles.forms import ArticleRestoreForm
from the_green_economics.apps.articles.forms import DeleteArticleForm
from the_green_economics.apps.articles.models import Article
from the_green_economics.apps.utils.mixins import AdminUserMixin
from the_green_economics.apps.utils.mixins import PaginatedFilteredListView
from the_green_economics.apps.utils.models import PublicationStatus

DASHBOARD_ARTICLES_QUERYSET = Article.objects.filter(
    Q(status=PublicationStatus.PUBLISHED)
    | Q(status=PublicationStatus.DRAFT)
    | Q(status=PublicationStatus.UNDER_REVIEW),
).order_by("-updated_at")


class DashboardArticleListView(AdminUserMixin, PaginatedFilteredListView):
    model = Article
    template_name = "dashboards/articles/article_list.html"
    context_object_name = "articles"
    queryset = DASHBOARD_ARTICLES_QUERYSET
    filterset_class = ArticleFilter
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
    success_url = reverse_lazy("dashboards:article-list")
    queryset = DASHBOARD_ARTICLES_QUERYSET


dashboard_article_create_view = DashboardArticleCreateView.as_view()


class DashboardArticleUpdateView(AdminUserMixin, UpdateView):
    model = Article
    form_class = ArticleForm
    template_name = "dashboards/articles/article_update.html"
    success_url = reverse_lazy("dashboards:article-list")
    slug_url_kwarg = "slug"
    context_object_name = "article"
    queryset = DASHBOARD_ARTICLES_QUERYSET

    def get_initial(self):
        """Set initial data for the form."""
        initial = super().get_initial()
        if self.form_class is None:
            return initial
        for field in self.form_class.base_fields:
            if field not in initial and self.object:
                initial[field] = getattr(self.object, field, None)
        return initial


dashboard_article_update_view = DashboardArticleUpdateView.as_view()


class DashboardArticleDeleteView(AdminUserMixin, DeleteView):
    model = Article
    form_class = DeleteArticleForm
    template_name = "dashboards/articles/article_delete.html"
    context_object_name = "article"
    success_url = reverse_lazy("dashboards:article-list")
    slug_url_kwarg = "slug"
    queryset = DASHBOARD_ARTICLES_QUERYSET

    def form_valid(self, form):
        success_url = self.get_success_url()
        self.object = self.get_object()
        self.object.status = PublicationStatus.ARCHIVED
        self.object.save()
        return redirect(success_url)


dashboard_article_delete_view = DashboardArticleDeleteView.as_view()


class DashboardArticleListArchivedView(AdminUserMixin, PaginatedFilteredListView):
    model = Article
    template_name = "dashboards/articles/article_list_archived.html"
    context_object_name = "articles"
    queryset = Article.objects.filter(status=PublicationStatus.ARCHIVED).order_by(
        "-updated_at",
    )
    filterset_class = ArticleFilter
    paginate_by = 10


dashboard_article_list_archived_view = DashboardArticleListArchivedView.as_view()


class DashboardArticleRestoreView(AdminUserMixin, UpdateView):
    model = Article
    form_class = ArticleRestoreForm
    template_name = "dashboards/articles/article_restore.html"
    success_url = reverse_lazy("dashboards:article-list")
    slug_url_kwarg = "slug"
    context_object_name = "article"
    queryset = Article.objects.filter(status=PublicationStatus.ARCHIVED).order_by(
        "-updated_at",
    )


dashboard_article_restore_view = DashboardArticleRestoreView.as_view()
