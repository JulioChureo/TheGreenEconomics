from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.generic import DetailView

from the_green_economics.apps.articles.filters import ArticleFilter
from the_green_economics.apps.articles.forms import Article
from the_green_economics.apps.utils.mixins import PaginatedFilteredListView

ARTICLES_QUERYSET = Article.objects.filter(
    status=Article.Status.PUBLISHED,
).order_by("-publication_date")


# Vistas para Artículos Científicos
# @method_decorator(cache_page(timeout=60, key_prefix="articles-list-"), name="dispatch")
class ArticleListView(PaginatedFilteredListView):
    model = Article
    template_name = "articles/articles_list.html"
    context_object_name = "articles"
    paginate_by = 10
    queryset = ARTICLES_QUERYSET
    filterset_class = ArticleFilter

    def get_queryset(self):
        return list(
            super().get_queryset().values("id", "title", "slug", "publication_date"),
        )


article_list_view = ArticleListView.as_view()


@method_decorator(
    cache_page(timeout=60, key_prefix="articles-detail-"),
    name="dispatch",
)
class ArticleDetailView(DetailView):
    model = Article
    template_name = "articles/articles_detail.html"
    context_object_name = "article"
    slug_url_kwarg = "slug"
    queryset = ARTICLES_QUERYSET


article_detail_view = ArticleDetailView.as_view()
