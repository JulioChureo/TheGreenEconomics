from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.views.generic import DeleteView
from django.views.generic import DetailView
from django.views.generic import ListView
from django.views.generic import UpdateView

from the_green_economics.apps.articles.forms import ArticleForm
from the_green_economics.apps.articles.forms import DeleteArticleForm
from the_green_economics.apps.articles.models import Article


class DashboardArticleListView(ListView):
    model = Article
    template_name = "dashboards/articles/article_list.html"
    context_object_name = "articles"

    def get_queryset(self):
        return Article.objects.filter().order_by(
            "-publication_date",
        )


dashboard_article_list_view = DashboardArticleListView.as_view()


class DashboardArticleDetailView(DetailView):
    model = Article
    template_name = "dashboards/articles/article_retrieve.html"
    context_object_name = "article"
    slug_url_kwarg = "slug"

    def get_queryset(self):
        return Article.objects.all()


dashboard_article_detail_view = DashboardArticleDetailView.as_view()


class DashboardArticleCreateView(CreateView):
    model = Article
    form_class = ArticleForm
    template_name = "dashboards/articles/article_create.html"
    success_url = reverse_lazy("articles:list")


dashboard_article_create_view = DashboardArticleCreateView.as_view()


class DashboardArticleUpdateView(UpdateView):
    model = Article
    form_class = ArticleForm
    template_name = "dashboards/articles/article_update.html"
    success_url = reverse_lazy("articles:list")
    slug_url_kwarg = "slug"

    def get_queryset(self):
        return Article.objects.all()


dashboard_article_update_view = DashboardArticleUpdateView.as_view()


class DashboardArticleDeleteView(DeleteView):
    model = Article
    form_class = DeleteArticleForm
    template_name = "dashboards/articles/article_delete.html"
    success_url = reverse_lazy("articles:list")
    slug_url_kwarg = "slug"

    def get_queryset(self):
        return Article.objects.all()


dashboard_article_delete_view = DashboardArticleDeleteView.as_view()
