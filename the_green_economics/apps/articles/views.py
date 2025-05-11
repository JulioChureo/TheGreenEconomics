from django.views.generic import DetailView
from django.views.generic import ListView

from the_green_economics.apps.articles.forms import Article


# Vistas para Artículos Científicos
class ArticleListView(ListView):
    model = Article
    template_name = "articles/articles_list.html"
    context_object_name = "articles"
    paginate_by = 10

    def get_queryset(self):
        if self.request.user.is_staff:
            return Article.objects.all().order_by("-publication_date")
        return Article.objects.filter().order_by(
            "-publication_date",
        )


class ArticleDetailView(DetailView):
    model = Article
    template_name = "articles/articles_detail.html"
    context_object_name = "article"
    slug_url_kwarg = "slug"

    def get_queryset(self):
        if self.request.user.is_staff:
            return Article.objects.all()
        return Article.objects.filter()
