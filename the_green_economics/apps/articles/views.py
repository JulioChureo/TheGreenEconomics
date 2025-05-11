from django.views.generic import DetailView
from django.views.generic import ListView

from the_green_economics.apps.articles.forms import Article

ARTICLES_QUERYSET = Article.objects.filter(
    #    status=Article.Status.PUBLISHED,
).order_by("-publication_date")


# Vistas para Artículos Científicos
class ArticleListView(ListView):
    model = Article
    template_name = "articles/articles_list.html"
    context_object_name = "articles"
    paginate_by = 10
    queryset = ARTICLES_QUERYSET


class ArticleDetailView(DetailView):
    model = Article
    template_name = "articles/articles_detail.html"
    context_object_name = "article"
    slug_url_kwarg = "slug"
    queryset = ARTICLES_QUERYSET
